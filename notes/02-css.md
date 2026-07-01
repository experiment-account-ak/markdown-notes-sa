# Sass Variables vs. CSS Custom Properties

Variables can also be used in native CSS using **custom properties**:

- A custom property is defined in the form `--name-of-property: value`
- It is used by means of `var(--name-of-property)`

- [+] Advantage compared with Sass variables: custom properties are retained at runtime
- [>] Custom properties are taken into account by the cascade
- [>] Custom properties can be manipulated through JavaScript

---

# Flexbox Quick Reference

Use Flexbox when items should be arranged mainly in one direction.

```css
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
```

Common properties:

- `display: flex`
- `flex-direction`
- `justify-content`
- `align-items`
- `gap`
- `flex-wrap`

---

# CSS Grid Quick Reference

Grid is useful when rows and columns both matter.

```css
.dashboard {
  display: grid;
  grid-template-columns: 18rem 1fr;
  gap: 1.5rem;
}
```

| Tool | Best suited for |
|---|---|
| Flexbox | One-dimensional layouts |
| Grid | Two-dimensional layouts |
| Positioning | Overlays and anchored elements |
