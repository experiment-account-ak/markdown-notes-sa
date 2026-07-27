# Web Architecture Lecture Scenario Questions and Answers

## 1. Scenario: Architectural Selection (MPA vs. SPA)

**Scenario:** A startup is developing two different applications:
*   **Project A:** A simple company website that presents static information about services and contact details.
*   **Project B:** A complex web-based spreadsheet application that requires real-time calculations, heavy user interaction, and a desktop-like feel.

**Questions:**
*   Based on the definitions in the lecture, which architectural style (MPA or SPA) would you recommend for each project, and why?[cite: 1]
*   What is a major challenge the team for "Project B" might face regarding SEO compared to "Project A" if they choose a pure client-side rendering approach?[cite: 1]

### Answer

*   **Recommendation:**
    *   **Project A:** You should use a **Multi-Page Application (MPA)**. Because the content is static and informational, an MPA provides faster initial loading times and better SEO by default, as the server delivers complete HTML pages for each route[cite: 1].
    *   **Project B:** You should use a **Single-Page Application (SPA)**. Complex applications like a spreadsheet require maintaining state across user actions without page reloads, which is the primary strength of the SPA architecture[cite: 1].
*   **SEO Challenge:** If Project B uses a pure client-side rendering (CSR) approach, it may struggle with SEO because search engine crawlers might not execute the JavaScript necessary to generate the page content. This can lead to the crawler seeing an empty page, preventing the content from being indexed correctly[cite: 1].

## 2. Scenario: Rendering Strategy Trade-offs

**Scenario:** You are a lead engineer tasked with optimizing the performance of a high-traffic news website. The site needs to be highly interactive, but it is crucial that the content appears on the user's screen as quickly as possible.

**Questions:**
*   If you implement **Client-Side Rendering (CSR)**, what are the potential trade-offs regarding the **Time to Interactive (TTI)** and **First Contentful Paint (FCP)**?[cite: 1]
*   How would the introduction of **Server-Side Rendering (SSR)** (specifically with rehydration) change the way the browser displays content compared to pure CSR?[cite: 1]
*   If you wanted the absolute fastest **Time to First Byte (TTFB)** for pages that do not change frequently, which rendering approach (from the overview table) would be most suitable?[cite: 1]

### Answer

*   **CSR Trade-offs:**
    *   **Time to Interactive (TTI):** TTI is often negatively impacted in CSR because the browser must download the full JavaScript bundle and execute it before the user can interact with the page[cite: 1].
    *   **First Contentful Paint (FCP):** FCP is often slower because the user typically sees a blank screen or a loading spinner while the browser fetches and processes the data required to render the initial content[cite: 1].
*   **SSR (with Rehydration) Impact:**
    *   SSR allows the server to send the fully rendered HTML to the browser immediately, significantly improving the **First Contentful Paint** because the user sees content faster[cite: 1].
    *   **Rehydration** occurs after the initial load, where the JavaScript "attaches" itself to the static HTML to enable interactivity. This bridges the gap, allowing the page to be visible quickly while eventually becoming a fully dynamic application[cite: 1].
*   **Fastest Time to First Byte (TTFB):**
    *   For pages that do not change frequently, **Server-Side Rendering (SSR)** or **Static Site Generation (SSG)** is most suitable. These methods allow the server to deliver a ready-to-view HTML file immediately upon request, minimizing the delay before the first byte arrives[cite: 1].

## 3. Scenario: Task Distribution and AJAX

**Scenario:** You have a legacy Multi-Page Application (MPA) where clicking every menu item causes a full page reload, leading to a poor user experience. You decide to integrate AJAX to improve the "live search" functionality where suggestions appear as the user types.

**Questions:**
*   How does the **task distribution** change between the client and the server once you move from a classic MPA to an "MPA + AJAX" architecture?[cite: 1]
*   Explain the role of the browser in this new scenario: When the user types a letter, what happens to the browser's "blocking" behavior compared to the classic request-response cycle?[cite: 1]
*   Why is the **XMLHttpRequest** or **Fetch API** considered a prerequisite for this improvement?[cite: 1]

### Answer

*   **Task Distribution:**
    *   In a classic MPA, the server is responsible for rendering the full UI (view) and managing application state. Moving to an "MPA + AJAX" architecture shifts the responsibility of UI updates to the client[cite: 1]. The server transitions into an API-centric role, providing raw data (often JSON) rather than pre-rendered HTML[cite: 1].
*   **Browser "Blocking" Behavior:**
    *   In a traditional request-response cycle, the browser blocks user interaction during the "loading" phase of a page navigation, essentially freezing the experience while it waits for a new page to arrive[cite: 1].
    *   With AJAX, the browser performs background requests. Because these requests occur in the background, the UI remains unblocked, allowing the user to continue interacting with the page while data is being fetched[cite: 1].
*   **Role of Fetch API/XMLHttpRequest:**
    *   These APIs are essential because they are the technical mechanisms that allow the browser to initiate HTTP requests programmatically from the client-side JavaScript[cite: 1]. Without them, the browser would have no way to communicate with the server to fetch data without triggering a full-page browser refresh[cite: 1].
