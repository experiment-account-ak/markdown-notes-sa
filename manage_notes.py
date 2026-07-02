#!/usr/bin/env python3
"""Terminal manager and local server for the Markdown Notes project.

Run without arguments for the easiest workflow:

    python manage_notes.py

That starts the web app, opens it in the default browser, and shows an
interactive menu for adding, renaming, moving, reordering, and deleting notes.

The script uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import threading
import time
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent
NOTES_DIR = PROJECT_ROOT / "notes"
INDEX_FILE = NOTES_DIR / "index.json"
SUPPORTED_SUFFIXES = {".md", ".markdown"}
DEFAULT_PORT = 8000


class NotesManagerError(Exception):
    """A user-facing error raised by the note manager."""


class QuietRequestHandler(SimpleHTTPRequestHandler):
    """Serve the project without printing every request to the terminal."""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def note_filename(entry: Any) -> str:
    """Return the Markdown filename from an old or new manifest entry."""
    if isinstance(entry, str) and entry.strip():
        return entry.strip()
    if isinstance(entry, dict) and isinstance(entry.get("file"), str):
        filename = entry["file"].strip()
        if filename:
            return filename
    raise NotesManagerError("Invalid note entry in notes/index.json.")


def note_custom_title(entry: Any) -> str | None:
    """Return a custom sidebar title when one is configured."""
    if not isinstance(entry, dict):
        return None
    title = entry.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return None


def make_note_entry(filename: str, title: str | None) -> dict[str, str]:
    entry = {"file": filename}
    if title and title.strip():
        entry["title"] = title.strip()
    return entry


def load_manifest() -> dict[str, Any]:
    if not INDEX_FILE.exists():
        return {"sections": []}

    try:
        with INDEX_FILE.open("r", encoding="utf-8") as file:
            manifest = json.load(file)
    except json.JSONDecodeError as error:
        raise NotesManagerError(
            f"Cannot read {INDEX_FILE.relative_to(PROJECT_ROOT)}: invalid JSON "
            f"at line {error.lineno}, column {error.colno}."
        ) from error

    if not isinstance(manifest, dict) or not isinstance(manifest.get("sections"), list):
        raise NotesManagerError(
            f"{INDEX_FILE.relative_to(PROJECT_ROOT)} must contain a 'sections' array."
        )

    for section_position, section in enumerate(manifest["sections"], start=1):
        if not isinstance(section, dict):
            raise NotesManagerError(
                f"Section {section_position} in index.json is not an object."
            )
        if not isinstance(section.get("title"), str) or not section["title"].strip():
            raise NotesManagerError(f"Section {section_position} needs a non-empty title.")
        if not isinstance(section.get("files"), list):
            raise NotesManagerError(f"Section {section_position} needs a 'files' array.")

        for note_position, entry in enumerate(section["files"], start=1):
            try:
                note_filename(entry)
            except NotesManagerError as error:
                raise NotesManagerError(
                    f"Note {note_position} in section {section_position} is invalid."
                ) from error
            if isinstance(entry, dict):
                title = entry.get("title")
                if title is not None and (
                    not isinstance(title, str) or not title.strip()
                ):
                    raise NotesManagerError(
                        f"Note {note_position} in section {section_position} has an invalid 'title'."
                    )

    return manifest


def save_manifest(manifest: dict[str, Any]) -> None:
    """Write index.json atomically and keep a one-file backup."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    if INDEX_FILE.exists():
        shutil.copy2(INDEX_FILE, INDEX_FILE.with_suffix(".json.bak"))

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="\n",
        dir=NOTES_DIR,
        prefix=".index-",
        suffix=".tmp",
        delete=False,
    ) as temporary:
        json.dump(manifest, temporary, indent=2, ensure_ascii=False)
        temporary.write("\n")
        temporary_path = Path(temporary.name)

    temporary_path.replace(INDEX_FILE)


def registered_files(manifest: dict[str, Any]) -> list[str]:
    return [
        note_filename(entry)
        for section in manifest["sections"]
        for entry in section["files"]
    ]


# ---------------------------------------------------------------------------
# Text, path, and prompt helpers
# ---------------------------------------------------------------------------


def normalize_input_path(raw_path: str) -> Path:
    """Accept ordinary paths and paths dragged into common terminal programs."""
    value = raw_path.strip().strip('"').strip("'")
    value = value.replace("\\ ", " ")
    return Path(value).expanduser().resolve()


def validate_source(path: Path) -> None:
    if not path.exists():
        raise NotesManagerError(f"File not found: {path}")
    if not path.is_file():
        raise NotesManagerError(f"Not a file: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        allowed = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise NotesManagerError(f"Expected a Markdown file ({allowed}), received: {path.name}")

    try:
        path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise NotesManagerError(
            f"{path.name} is not UTF-8 encoded. Save it as UTF-8 and try again."
        ) from error


def slugify_stem(value: str) -> str:
    value = Path(value).stem.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-") or "note"


def slugify_filename(path: Path) -> str:
    return f"{slugify_stem(path.name)}.md"


def validate_new_filename(raw_name: str) -> str:
    filename = f"{slugify_stem(raw_name)}.md"
    destination = NOTES_DIR / filename
    if destination.exists():
        raise NotesManagerError(f"notes/{filename} already exists.")
    return filename


def unique_destination(source: Path) -> Path:
    base = slugify_stem(source.name)
    candidate = NOTES_DIR / f"{base}.md"
    counter = 2

    while candidate.exists():
        try:
            if candidate.samefile(source):
                return candidate
        except OSError:
            pass
        candidate = NOTES_DIR / f"{base}-{counter}.md"
        counter += 1

    return candidate


def first_markdown_heading(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    for line in lines:
        match = re.match(r"^\s*#{1,3}\s+(.+?)\s*#*\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def friendly_stem(path_or_name: Path | str) -> str:
    path = Path(path_or_name)
    value = re.sub(r"[-_]+", " ", path.stem).strip()
    return re.sub(r"\s+", " ", value).title() or "Untitled Note"


def note_display_title(entry: Any) -> str:
    custom = note_custom_title(entry)
    if custom:
        return custom
    filename = note_filename(entry)
    return first_markdown_heading(NOTES_DIR / filename) or friendly_stem(filename)


def note_label(entry: Any) -> str:
    filename = note_filename(entry)
    return f"{note_display_title(entry)} [{filename}]"


def prompt_non_empty(label: str, default: str | None = None) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("Please enter a value.")


def prompt_integer(label: str, minimum: int, maximum: int, default: int) -> int:
    while True:
        value = input(f"{label} [{default}]: ").strip()
        if not value:
            return default
        try:
            number = int(value)
        except ValueError:
            print(f"Enter a number from {minimum} to {maximum}.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"Enter a number from {minimum} to {maximum}.")


def prompt_yes_no(label: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} [{suffix}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Enter y or n.")


def confirm_phrase(label: str, phrase: str) -> bool:
    value = input(f"{label}\nType {phrase!r} to confirm: ").strip()
    return value == phrase


# ---------------------------------------------------------------------------
# Selection helpers
# ---------------------------------------------------------------------------


def choose_section(
    manifest: dict[str, Any],
    *,
    label: str = "Section",
    allow_create: bool = False,
    suggested_title: str | None = None,
    exclude_index: int | None = None,
) -> int:
    sections = manifest["sections"]
    available = [
        (index, section)
        for index, section in enumerate(sections)
        if index != exclude_index
    ]

    if not available and not allow_create:
        raise NotesManagerError("No suitable sections are available.")

    print(f"\nChoose {label.lower()}:")
    for display_number, (_, section) in enumerate(available, start=1):
        count = len(section["files"])
        noun = "note" if count == 1 else "notes"
        print(f"  {display_number}. {section['title']} ({count} {noun})")

    create_number = len(available) + 1
    if allow_create:
        print(f"  {create_number}. Create a new section")

    maximum = create_number if allow_create else len(available)
    choice = prompt_integer(label, 1, maximum, maximum if allow_create else 1)

    if allow_create and choice == create_number:
        title = prompt_non_empty("New section title", suggested_title or "New Section")
        sections.append({"title": title, "files": []})
        return len(sections) - 1

    return available[choice - 1][0]


def choose_note_in_section(
    section: dict[str, Any],
    *,
    label: str = "Note",
) -> int:
    files = section["files"]
    if not files:
        raise NotesManagerError(f"'{section['title']}' does not contain any notes.")

    print(f"\nNotes in '{section['title']}':")
    for number, entry in enumerate(files, start=1):
        print(f"  {number}. {note_label(entry)}")

    return prompt_integer(label, 1, len(files), 1) - 1


def choose_note(manifest: dict[str, Any]) -> tuple[int, int]:
    non_empty = [
        (index, section)
        for index, section in enumerate(manifest["sections"])
        if section["files"]
    ]
    if not non_empty:
        raise NotesManagerError("There are no notes to choose from.")

    print("\nChoose a section:")
    for number, (_, section) in enumerate(non_empty, start=1):
        count = len(section['files'])
        noun = "note" if count == 1 else "notes"
        print(f"  {number}. {section['title']} ({count} {noun})")

    section_choice = prompt_integer("Section", 1, len(non_empty), 1) - 1
    section_index = non_empty[section_choice][0]
    note_index = choose_note_in_section(manifest["sections"][section_index])
    return section_index, note_index


def choose_insert_position(
    section: dict[str, Any],
    *,
    label: str = "Position",
    entries: Iterable[Any] | None = None,
) -> int:
    files = list(section["files"] if entries is None else entries)
    if files:
        print(f"\nCurrent order in '{section['title']}':")
        for number, entry in enumerate(files, start=1):
            print(f"  {number}. {note_label(entry)}")
    else:
        print(f"\n'{section['title']}' is currently empty.")

    maximum = len(files) + 1
    position = prompt_integer(label, 1, maximum, maximum)
    return position - 1


# ---------------------------------------------------------------------------
# Note operations
# ---------------------------------------------------------------------------


def collect_sources(arguments: list[str]) -> list[Path]:
    if arguments:
        return [normalize_input_path(value) for value in arguments]

    print("Drag a Markdown file into this terminal, or paste its path.")
    raw_path = prompt_non_empty("Markdown file")
    return [normalize_input_path(raw_path)]


def import_note(source: Path, manifest: dict[str, Any]) -> tuple[str, str, str, int]:
    validate_source(source)

    destination = unique_destination(source)
    filename = destination.name
    if filename in set(registered_files(manifest)):
        raise NotesManagerError(f"{filename} is already registered in notes/index.json.")

    print(f"\nImporting: {source.name}")
    print(f"Stored as: notes/{filename}")

    suggested_display_name = first_markdown_heading(source) or friendly_stem(source)
    display_name = prompt_non_empty(
        "Name shown inside the section",
        suggested_display_name,
    )

    section_index = choose_section(
        manifest,
        label="Section",
        allow_create=True,
        suggested_title=suggested_display_name,
    )
    section = manifest["sections"][section_index]
    insert_at = choose_insert_position(section, label="Place the new note at position")
    entry = make_note_entry(filename, display_name)

    copied = False
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            is_same_file = destination.exists() and destination.samefile(source)
        except OSError:
            is_same_file = False

        if not is_same_file:
            shutil.copy2(source, destination)
            copied = True

        section["files"].insert(insert_at, entry)
        save_manifest(manifest)
    except Exception:
        if copied:
            destination.unlink(missing_ok=True)
        if entry in section["files"]:
            section["files"].remove(entry)
        raise

    return filename, display_name, section["title"], insert_at + 1


def rename_note(manifest: dict[str, Any]) -> None:
    section_index, note_index = choose_note(manifest)
    section = manifest["sections"][section_index]
    old_entry = section["files"][note_index]
    old_filename = note_filename(old_entry)
    old_title = note_display_title(old_entry)

    print(f"\nRenaming: {old_title} [{old_filename}]")
    new_title = prompt_non_empty("New sidebar name", old_title)
    new_filename = old_filename

    rename_file = prompt_yes_no("Also rename the stored Markdown filename?", False)
    old_path = NOTES_DIR / old_filename
    new_path = old_path

    if rename_file:
        suggested = Path(old_filename).stem
        requested = prompt_non_empty("New filename", suggested)
        candidate = f"{slugify_stem(requested)}.md"
        if candidate != old_filename:
            new_filename = validate_new_filename(candidate)
            new_path = NOTES_DIR / new_filename

    old_entry_copy = old_entry
    file_was_renamed = False
    try:
        if new_path != old_path:
            if not old_path.exists():
                raise NotesManagerError(f"Cannot rename missing file: notes/{old_filename}")
            old_path.rename(new_path)
            file_was_renamed = True

        section["files"][note_index] = make_note_entry(new_filename, new_title)
        save_manifest(manifest)
    except Exception:
        section["files"][note_index] = old_entry_copy
        if file_was_renamed and new_path.exists():
            new_path.rename(old_path)
        raise

    print(f"Renamed to: {new_title} [notes/{new_filename}]")


def move_note(manifest: dict[str, Any]) -> None:
    source_section_index, note_index = choose_note(manifest)
    source_section = manifest["sections"][source_section_index]
    entry = source_section["files"][note_index]

    print(f"\nMoving: {note_label(entry)}")
    destination_section_index = choose_section(
        manifest,
        label="Destination section",
        allow_create=True,
        suggested_title="New Section",
    )
    destination_section = manifest["sections"][destination_section_index]

    if destination_section_index == source_section_index:
        remaining = [
            item for index, item in enumerate(source_section["files"]) if index != note_index
        ]
        insert_at = choose_insert_position(
            destination_section,
            label="New position",
            entries=remaining,
        )
    else:
        insert_at = choose_insert_position(destination_section, label="Position in destination")

    removed = source_section["files"].pop(note_index)
    destination_section["files"].insert(insert_at, removed)
    try:
        save_manifest(manifest)
    except Exception:
        destination_section["files"].pop(insert_at)
        source_section["files"].insert(note_index, removed)
        raise

    print(
        f"Moved to '{destination_section['title']}' at position {insert_at + 1}."
    )


def reorder_note(manifest: dict[str, Any]) -> None:
    section_index = choose_section(manifest, label="Section")
    section = manifest["sections"][section_index]
    note_index = choose_note_in_section(section)
    entry = section["files"][note_index]

    remaining = [item for index, item in enumerate(section["files"]) if index != note_index]
    new_index = choose_insert_position(section, label="New position", entries=remaining)

    section["files"].pop(note_index)
    section["files"].insert(new_index, entry)
    try:
        save_manifest(manifest)
    except Exception:
        section["files"].pop(new_index)
        section["files"].insert(note_index, entry)
        raise

    print(f"Moved '{note_display_title(entry)}' to position {new_index + 1}.")


def delete_note(manifest: dict[str, Any]) -> None:
    section_index, note_index = choose_note(manifest)
    section = manifest["sections"][section_index]
    entry = section["files"][note_index]
    filename = note_filename(entry)
    title = note_display_title(entry)

    print(f"\nDelete: {title} [notes/{filename}]")
    if not confirm_phrase("This removes the note from the app.", "DELETE"):
        print("Cancelled.")
        return

    other_references = registered_files(manifest).count(filename) > 1
    delete_file = False
    if other_references:
        print("The same Markdown file is referenced elsewhere, so it will not be deleted.")
    else:
        delete_file = prompt_yes_no("Also delete the Markdown file from notes/?", True)

    path = NOTES_DIR / filename
    staged_path: Path | None = None
    removed = section["files"].pop(note_index)

    try:
        if delete_file and path.exists():
            staged_path = NOTES_DIR / f".deleted-{time.time_ns()}-{path.name}"
            path.rename(staged_path)

        save_manifest(manifest)

        if staged_path is not None:
            staged_path.unlink(missing_ok=True)
    except Exception:
        section["files"].insert(note_index, removed)
        if staged_path is not None and staged_path.exists():
            staged_path.rename(path)
        raise

    print(f"Deleted '{title}'.")


# ---------------------------------------------------------------------------
# Section operations
# ---------------------------------------------------------------------------


def rename_section(manifest: dict[str, Any]) -> None:
    section_index = choose_section(manifest, label="Section")
    section = manifest["sections"][section_index]
    old_title = section["title"]
    new_title = prompt_non_empty("New section name", old_title)
    section["title"] = new_title
    try:
        save_manifest(manifest)
    except Exception:
        section["title"] = old_title
        raise
    print(f"Renamed section to '{new_title}'.")


def reorder_section(manifest: dict[str, Any]) -> None:
    sections = manifest["sections"]
    if len(sections) < 2:
        raise NotesManagerError("At least two sections are needed to reorder them.")

    section_index = choose_section(manifest, label="Section")
    section = sections[section_index]
    remaining = [item for index, item in enumerate(sections) if index != section_index]

    print("\nRemaining section order:")
    for number, item in enumerate(remaining, start=1):
        print(f"  {number}. {item['title']}")

    new_index = prompt_integer("New section position", 1, len(remaining) + 1, len(remaining) + 1) - 1
    sections.pop(section_index)
    sections.insert(new_index, section)
    try:
        save_manifest(manifest)
    except Exception:
        sections.pop(new_index)
        sections.insert(section_index, section)
        raise

    print(f"Moved section '{section['title']}' to position {new_index + 1}.")


def delete_section(manifest: dict[str, Any]) -> None:
    section_index = choose_section(manifest, label="Section")
    section = manifest["sections"][section_index]
    title = section["title"]
    files = list(section["files"])

    print(f"\nDelete section: {title}")
    print(f"This section contains {len(files)} note(s).")
    if not confirm_phrase("This removes the entire section from the app.", "DELETE SECTION"):
        print("Cancelled.")
        return

    delete_files = False
    if files:
        delete_files = prompt_yes_no(
            "Also delete its Markdown files when they are not used elsewhere?",
            False,
        )

    all_references = registered_files(manifest)
    staged: list[tuple[Path, Path]] = []
    removed = manifest["sections"].pop(section_index)

    try:
        if delete_files:
            for entry in files:
                filename = note_filename(entry)
                if all_references.count(filename) > 1:
                    continue
                path = NOTES_DIR / filename
                if path.exists():
                    staged_path = NOTES_DIR / f".deleted-{time.time_ns()}-{path.name}"
                    path.rename(staged_path)
                    staged.append((path, staged_path))

        save_manifest(manifest)

        for _, staged_path in staged:
            staged_path.unlink(missing_ok=True)
    except Exception:
        manifest["sections"].insert(section_index, removed)
        for original, staged_path in staged:
            if staged_path.exists():
                staged_path.rename(original)
        raise

    print(f"Deleted section '{title}'.")


# ---------------------------------------------------------------------------
# Listing and project checks
# ---------------------------------------------------------------------------


def list_notes(manifest: dict[str, Any]) -> None:
    sections = manifest["sections"]
    if not sections:
        print("No sections are configured.")
        return

    print()
    for section_number, section in enumerate(sections, start=1):
        print(f"{section_number}. {section['title']}")
        if not section["files"]:
            print("   (empty)")
            continue
        for note_number, entry in enumerate(section["files"], start=1):
            print(f"   {note_number}. {note_label(entry)}")


def check_project(manifest: dict[str, Any]) -> bool:
    references = registered_files(manifest)
    missing = sorted({filename for filename in references if not (NOTES_DIR / filename).is_file()})
    duplicates = sorted({filename for filename in references if references.count(filename) > 1})
    actual = {
        path.name
        for path in NOTES_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    }
    orphaned = sorted(actual - set(references))

    print("\nProject check")
    print(f"  Sections: {len(manifest['sections'])}")
    print(f"  Registered notes: {len(references)}")

    if missing:
        print("\nMissing Markdown files:")
        for filename in missing:
            print(f"  - notes/{filename}")

    if duplicates:
        print("\nFiles referenced more than once:")
        for filename in duplicates:
            print(f"  - notes/{filename}")

    if orphaned:
        print("\nMarkdown files not registered in index.json:")
        for filename in orphaned:
            print(f"  - notes/{filename}")

    healthy = not missing and not duplicates and not orphaned
    if healthy:
        print("\nEverything looks good.")
    return healthy


# ---------------------------------------------------------------------------
# Server helpers
# ---------------------------------------------------------------------------


def create_server(port: int) -> tuple[ThreadingHTTPServer, int]:
    handler = partial(QuietRequestHandler, directory=str(PROJECT_ROOT))
    last_error: OSError | None = None
    for candidate in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), handler)
            return server, candidate
        except OSError as error:
            last_error = error
    raise NotesManagerError(
        f"Could not start the server on ports {port}-{port + 19}: {last_error}"
    )


def open_browser_later(url: str) -> None:
    def _open() -> None:
        webbrowser.open(url)

    timer = threading.Timer(0.35, _open)
    timer.daemon = True
    timer.start()


def start_background_server(port: int, open_browser: bool) -> tuple[ThreadingHTTPServer, str]:
    server, actual_port = create_server(port)
    url = f"http://127.0.0.1:{actual_port}/"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    if open_browser:
        open_browser_later(url)
    return server, url


def serve_forever(port: int, open_browser: bool) -> int:
    server, actual_port = create_server(port)
    url = f"http://127.0.0.1:{actual_port}/"
    print(f"Markdown Notes is running at {url}")
    print("Press Ctrl+C to stop the server.")
    if open_browser:
        open_browser_later(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


# ---------------------------------------------------------------------------
# Interactive dashboard
# ---------------------------------------------------------------------------


def print_menu(url: str) -> None:
    print("\n" + "=" * 62)
    print("Markdown Notes Manager")
    print(f"App: {url}")
    print("=" * 62)
    print("  1. Add note")
    print("  2. Rename note")
    print("  3. Move note to another section")
    print("  4. Reorder note inside a section")
    print("  5. Delete note")
    print("  6. Rename section")
    print("  7. Reorder sections")
    print("  8. Delete section")
    print("  9. List current structure")
    print(" 10. Check project")
    print(" 11. Open app in browser")
    print("  0. Exit and stop server")


def interactive_dashboard(port: int, open_browser: bool) -> int:
    server, url = start_background_server(port, open_browser)
    print(f"\nMarkdown Notes started at {url}")
    if open_browser:
        print("Opening it in your browser...")

    try:
        while True:
            manifest = load_manifest()
            print_menu(url)
            choice = prompt_integer("Choose an action", 0, 11, 1)

            try:
                if choice == 0:
                    print("Stopping server. Goodbye.")
                    return 0
                if choice == 1:
                    sources = collect_sources([])
                    for source in sources:
                        filename, display_name, section_title, position = import_note(
                            source, manifest
                        )
                        print(
                            f"Added '{display_name}' to '{section_title}' at position "
                            f"{position} [notes/{filename}]."
                        )
                elif choice == 2:
                    rename_note(manifest)
                elif choice == 3:
                    move_note(manifest)
                elif choice == 4:
                    reorder_note(manifest)
                elif choice == 5:
                    delete_note(manifest)
                elif choice == 6:
                    rename_section(manifest)
                elif choice == 7:
                    reorder_section(manifest)
                elif choice == 8:
                    delete_section(manifest)
                elif choice == 9:
                    list_notes(manifest)
                elif choice == 10:
                    check_project(manifest)
                elif choice == 11:
                    webbrowser.open(url)

                if choice in {1, 2, 3, 4, 5, 6, 7, 8}:
                    print("Refresh the browser to see the change.")
            except NotesManagerError as error:
                print(f"Error: {error}", file=sys.stderr)
            except OSError as error:
                print(f"File error: {error}", file=sys.stderr)

            input("\nPress Enter to return to the menu...")
    finally:
        server.shutdown()
        server.server_close()


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Markdown notes and run the local web app."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"preferred local server port (default: {DEFAULT_PORT})",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="do not open the browser automatically",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("menu", help="start the app and open the interactive manager")
    subparsers.add_parser("serve", aliases=["start"], help="start only the local web server")

    add_parser = subparsers.add_parser("add", help="import one or more Markdown files")
    add_parser.add_argument("files", nargs="*", help="Markdown files to import")

    subparsers.add_parser("list", help="show sections and registered notes")
    subparsers.add_parser("rename", help="rename a note and optionally its file")
    subparsers.add_parser("move", help="move a note to another section")
    subparsers.add_parser("reorder", help="reorder a note inside its section")
    subparsers.add_parser("delete", help="delete a note")
    subparsers.add_parser("rename-section", help="rename a section")
    subparsers.add_parser("reorder-sections", help="change section order")
    subparsers.add_parser("delete-section", help="delete a section")
    subparsers.add_parser("check", help="check for missing, duplicate, or orphaned files")

    return parser


def run_command(args: argparse.Namespace) -> int:
    command = args.command
    open_browser = not args.no_browser

    if command is None or command == "menu":
        return interactive_dashboard(args.port, open_browser)
    if command in {"serve", "start"}:
        return serve_forever(args.port, open_browser)

    manifest = load_manifest()

    if command == "list":
        list_notes(manifest)
    elif command == "check":
        return 0 if check_project(manifest) else 1
    elif command == "add":
        imported = []
        for source in collect_sources(args.files):
            imported.append(import_note(source, manifest))
        print("\nDone.")
        for filename, display_name, section_title, position in imported:
            print(
                f"  {display_name} → {section_title} (position {position}) "
                f"[notes/{filename}]"
            )
    elif command == "rename":
        rename_note(manifest)
    elif command == "move":
        move_note(manifest)
    elif command == "reorder":
        reorder_note(manifest)
    elif command == "delete":
        delete_note(manifest)
    elif command == "rename-section":
        rename_section(manifest)
    elif command == "reorder-sections":
        reorder_section(manifest)
    elif command == "delete-section":
        delete_section(manifest)
    else:
        raise NotesManagerError(f"Unknown command: {command}")

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return run_command(args)
    except (NotesManagerError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
