(() => {
  "use strict";

  const state = {
    sections: [],
    slides: [],
    currentIndex: 0,
    searchQuery: ""
  };

  const elements = {
    sidebar: document.querySelector("#sidebar"),
    navigation: document.querySelector("#slide-navigation"),
    slide: document.querySelector("#slide"),
    counter: document.querySelector("#slide-counter"),
    sectionLabel: document.querySelector("#section-label"),
    slideTitle: document.querySelector("#slide-title"),
    previousButton: document.querySelector("#previous-button"),
    nextButton: document.querySelector("#next-button"),
    openSidebarButton: document.querySelector("#open-sidebar-button"),
    closeSidebarButton: document.querySelector("#close-sidebar-button"),
    themeButton: document.querySelector("#theme-button"),
    fullscreenButton: document.querySelector("#fullscreen-button"),
    searchInput: document.querySelector("#search-input")
  };

  async function loadText(path) {
    const response = await fetch(path);

    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}: ${path}`);
    }

    return response.text();
  }

  async function loadJson(path) {
    const response = await fetch(path);

    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}: ${path}`);
    }

    return response.json();
  }

  function splitMarkdownIntoSlides(markdown) {
    /*
      A line containing only three dashes separates slides.
      Dashes inside fenced code blocks are ignored.
    */
    const lines = markdown.replace(/\r\n?/g, "\n").split("\n");
    const chunks = [];
    let current = [];
    let insideCodeFence = false;

    for (const line of lines) {
      if (/^\s*```/.test(line)) {
        insideCodeFence = !insideCodeFence;
        current.push(line);
        continue;
      }

      if (!insideCodeFence && /^\s*---\s*$/.test(line)) {
        const value = current.join("\n").trim();

        if (value) {
          chunks.push(value);
        }

        current = [];
        continue;
      }

      current.push(line);
    }

    const lastValue = current.join("\n").trim();

    if (lastValue) {
      chunks.push(lastValue);
    }

    return chunks;
  }

  function getSlideTitle(markdown, fallback) {
    const match = markdown.match(/^\s*#{1,3}\s+(.+)$/m);
    return match ? match[1].trim() : fallback;
  }

  function stripMarkdown(markdown) {
    return markdown
      .replace(/```[\s\S]*?```/g, " ")
      .replace(/!\[[^\]]*]\([^)]*\)/g, " ")
      .replace(/\[([^\]]+)]\([^)]*\)/g, "$1")
      .replace(/[#>*_`~|()-]/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  async function loadNotes() {
    const manifest = await loadJson("notes/index.json");
    const sections = [];
    const slides = [];

    for (const sectionConfig of manifest.sections) {
      const section = {
        title: sectionConfig.title,
        slides: []
      };

      for (const noteConfig of sectionConfig.files) {
        const file = typeof noteConfig === "string"
          ? noteConfig
          : noteConfig.file;
        const customTitle = typeof noteConfig === "object" && noteConfig !== null
          && typeof noteConfig.title === "string"
          ? noteConfig.title.trim()
          : "";
        const markdown = await loadText(`notes/${file}`);
        const markdownSlides = splitMarkdownIntoSlides(markdown);

        markdownSlides.forEach((content, localIndex) => {
          const slide = {
            sectionTitle: section.title,
            title: localIndex === 0 && customTitle
              ? customTitle
              : getSlideTitle(
                  content,
                  `${section.title} ${localIndex + 1}`
                ),
            markdown: content,
            searchableText: stripMarkdown(content),
            file
          };

          slide.globalIndex = slides.length;
          section.slides.push(slide);
          slides.push(slide);
        });
      }

      sections.push(section);
    }

    state.sections = sections;
    state.slides = slides;

    const savedIndex = Number(localStorage.getItem("notes.currentSlide"));

    if (
      Number.isInteger(savedIndex) &&
      savedIndex >= 0 &&
      savedIndex < slides.length
    ) {
      state.currentIndex = savedIndex;
    }
  }

  function buildNavigation() {
    elements.navigation.innerHTML = "";

    const query = state.searchQuery.trim().toLowerCase();
    let visibleCount = 0;

    for (const section of state.sections) {
      const matchingSlides = section.slides.filter((slide) => {
        if (!query) {
          return true;
        }

        return (
          slide.title.toLowerCase().includes(query) ||
          slide.sectionTitle.toLowerCase().includes(query) ||
          slide.searchableText.includes(query)
        );
      });

      if (!matchingSlides.length) {
        continue;
      }

      visibleCount += matchingSlides.length;

      const sectionElement = document.createElement("section");
      sectionElement.className = "navigation-section";

      const heading = document.createElement("div");
      heading.className = "navigation-section-title";
      heading.textContent = section.title;
      sectionElement.appendChild(heading);

      for (const slide of matchingSlides) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "navigation-item";
        button.dataset.slideIndex = String(slide.globalIndex);

        const number = document.createElement("span");
        number.className = "navigation-number";
        number.textContent = `${slide.globalIndex + 1}.`;

        const title = document.createElement("span");
        title.className = "navigation-title";
        title.textContent = slide.title;

        button.append(number, title);

        button.addEventListener("click", () => {
          showSlide(slide.globalIndex);

          if (window.matchMedia("(max-width: 820px)").matches) {
            setSidebarOpen(false);
          }
        });

        sectionElement.appendChild(button);
      }

      elements.navigation.appendChild(sectionElement);
    }

    if (!visibleCount) {
      const message = document.createElement("p");
      message.className = "empty-navigation";
      message.textContent = "No slides match your search.";
      elements.navigation.appendChild(message);
    }

    updateActiveNavigationItem();
  }

  function updateActiveNavigationItem() {
    document.querySelectorAll(".navigation-item").forEach((item) => {
      const isActive =
        Number(item.dataset.slideIndex) === state.currentIndex;

      item.classList.toggle("active", isActive);

      if (isActive) {
        item.setAttribute("aria-current", "page");
      } else {
        item.removeAttribute("aria-current");
      }
    });

    document
      .querySelector(".navigation-item.active")
      ?.scrollIntoView({ block: "nearest" });
  }

  function showSlide(index) {
    if (index < 0 || index >= state.slides.length) {
      return;
    }

    state.currentIndex = index;

    const slide = state.slides[index];
    elements.slide.innerHTML = window.Markdown.render(slide.markdown);
    elements.slide.scrollTop = 0;

    elements.sectionLabel.textContent = slide.sectionTitle;
    elements.slideTitle.textContent = slide.title;
    elements.counter.textContent = `${index + 1} / ${state.slides.length}`;
    elements.previousButton.disabled = index === 0;
    elements.nextButton.disabled = index === state.slides.length - 1;

    document.title = `${slide.title} — Markdown Notes`;
    localStorage.setItem("notes.currentSlide", String(index));

    updateActiveNavigationItem();
  }

  function moveSlide(offset) {
    showSlide(state.currentIndex + offset);
  }

  function setSidebarOpen(isOpen) {
    elements.sidebar.classList.toggle("is-closed", !isOpen);
    localStorage.setItem("notes.sidebarOpen", String(isOpen));
  }

  function toggleTheme() {
    const current =
      document.documentElement.dataset.theme === "dark" ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";

    document.documentElement.dataset.theme = next;
    localStorage.setItem("notes.theme", next);
  }

  async function toggleFullscreen() {
    try {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
        document.body.classList.add("presentation-mode");
      } else {
        await document.exitFullscreen();
      }
    } catch (error) {
      console.error("Fullscreen could not be enabled:", error);
    }
  }

  function restorePreferences() {
    const savedTheme = localStorage.getItem("notes.theme");
    document.documentElement.dataset.theme =
      savedTheme === "dark" ? "dark" : "light";

    const savedSidebarOpen = localStorage.getItem("notes.sidebarOpen");
    const defaultOpen = !window.matchMedia("(max-width: 820px)").matches;
    const shouldOpen =
      savedSidebarOpen === null ? defaultOpen : savedSidebarOpen === "true";

    setSidebarOpen(shouldOpen);
  }

  function bindEvents() {
    elements.previousButton.addEventListener("click", () => moveSlide(-1));
    elements.nextButton.addEventListener("click", () => moveSlide(1));

    elements.openSidebarButton.addEventListener("click", () =>
      setSidebarOpen(true)
    );

    elements.closeSidebarButton.addEventListener("click", () =>
      setSidebarOpen(false)
    );

    elements.themeButton.addEventListener("click", toggleTheme);
    elements.fullscreenButton.addEventListener("click", toggleFullscreen);

    elements.searchInput.addEventListener("input", (event) => {
      state.searchQuery = event.target.value;
      buildNavigation();
    });

    document.addEventListener("fullscreenchange", () => {
      if (!document.fullscreenElement) {
        document.body.classList.remove("presentation-mode");
      }
    });

    document.addEventListener("keydown", (event) => {
      const active = document.activeElement;
      const typing =
        active instanceof HTMLInputElement ||
        active instanceof HTMLTextAreaElement ||
        active?.isContentEditable;

      if (typing) {
        if (event.key === "Escape") {
          active.blur();
        }
        return;
      }

      if (event.key === "ArrowRight" || event.key === "PageDown") {
        event.preventDefault();
        moveSlide(1);
      }

      if (event.key === "ArrowLeft" || event.key === "PageUp") {
        event.preventDefault();
        moveSlide(-1);
      }

      if (event.key === "Home") {
        event.preventDefault();
        showSlide(0);
      }

      if (event.key === "End") {
        event.preventDefault();
        showSlide(state.slides.length - 1);
      }

      if (event.key === "/") {
        event.preventDefault();
        setSidebarOpen(true);
        elements.searchInput.focus();
      }

      if (event.key.toLowerCase() === "f") {
        toggleFullscreen();
      }
    });
  }

  function showLoadingError(error) {
    console.error(error);

    elements.slide.innerHTML = `
      <div class="loading-error">
        <h1>Notes could not be loaded</h1>
        <p>
          Make sure you started a local web server instead of opening
          <code>index.html</code> directly.
        </p>
        <p>
          Run <code>python -m http.server 8000</code> in the project folder,
          then open <code>http://localhost:8000</code>.
        </p>
        <p><strong>Details:</strong> ${window.Markdown.escapeHtml(error.message)}</p>
      </div>
    `;
  }

  async function start() {
    restorePreferences();
    bindEvents();

    try {
      await loadNotes();
      buildNavigation();
      showSlide(state.currentIndex);
    } catch (error) {
      showLoadingError(error);
    }
  }

  start();
})();
