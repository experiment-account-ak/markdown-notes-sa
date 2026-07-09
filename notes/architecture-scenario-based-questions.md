# Architecture Scenario-Based Questions

[Source chat](https://chatgpt.com/g/g-p-6a295be0712c8191a00e1149bb7206ea/c/6a49062c-bafc-83eb-ad19-b118011f3599)

## 1. What architecture scenario-based exam questions can be framed from this module ❓

Below are **exam-style architecture scenario questions** from this Web Architectures / JavaScript APIs module. The main exam skill is: **given requirements, choose MPA, MPA + AJAX, SPA/CSR, Server Rendering, Static Rendering, SSR, or CSR with prerendering - and justify trade-offs.**

The lecture’s core decision question is: **where and when is the view constructed?** It compares server rendering, static rendering, CSR, and hybrid approaches such as SSR and CSR with prerendering. It also uses performance metrics such as **TTFB**, **FCP**, and **TTI** to judge architecture choices. `F-02-javascript-spas_en.pdf`
# Quick decision map

| Requirement in scenario | Likely architecture |
|---|---|
| Only navigation between pages, simple forms, little interaction | **Classic MPA / server rendering** |
| Existing MPA needs small dynamic widgets, like search suggestions | **MPA + AJAX** |
| Desktop-like app, long session, many interactions, no full reloads | **SPA / CSR** |
| Content rarely changes, fastest delivery, low runtime server work | **Static rendering** |
| Fast first visible page + later SPA behavior | **SSR / Universal Rendering** |
| SEO for SPA-like app, static initial view acceptable | **CSR with prerendering** |
| Strong reliability with minimal JavaScript dependency | Prefer **server rendering** or **static rendering**, not pure CSR |
| Highly personalized / behavior-driven / constantly changing content | Avoid pure **static rendering** |
# 1. Scenario: “A university department needs a website with Home, About, Contact, Staff, and News pages. The content changes rarely. The site should load very fast and should not require much server processing.”

## Which architecture should be chosen❓

**Answer: Static rendering.**

This is a content-driven website whose pages do not change frequently. Static rendering pre-generates all possible views during the build process, so at runtime the server already has complete HTML files and does not need to dynamically generate the page per request. This gives fast **TTFB**, because no dynamic rendering is needed, and fast **FCP/TTI** as long as the page does not include too much client-side JavaScript. `F-02-javascript-spas_en.pdf`

**Why not CSR?**  
CSR would require downloading and starting a JavaScript application even though the site mostly needs navigation and reading.

**Why not server rendering?**  
Server rendering would also work, but it does unnecessary dynamic work on every request if the content is mostly stable.

**Exam sentence:**  
For a rarely changing, content-driven website, static rendering is suitable because the HTML can be generated during build time and served quickly at runtime.
# 2. Scenario: “A company blog wants excellent initial load time and SEO. Articles are written by editors and published once or twice per week.”

## Which architecture should be chosen❓

**Answer: Static rendering.**

A blog is a classic content-driven application. The lecture explicitly mentions blogs and company websites as suitable examples for static rendering. The generated HTML can be served directly, giving fast TTFB, FCP, and TTI. `F-02-javascript-spas_en.pdf`

**Important limitation:**  
When an article changes, the site usually needs a **new build and deployment**. This is acceptable if publishing is not extremely frequent.

**Exam sentence:**  
Static rendering is appropriate because the content is stable enough to be pre-generated, and the user receives complete HTML immediately.
# 3. Scenario: “A stock trading dashboard shows constantly changing personalized data. Users interact with charts, filters, and live updates. SEO is irrelevant because the page is behind login.”

## Which architecture should be chosen❓

**Answer: SPA / client-side rendering, possibly with AJAX-based API communication.**

This is a behavior-driven and highly interactive application. A SPA fits because after the initial load, the page is not reloaded; instead, the view is updated through DOM manipulation, and server communication is mainly used to load data or execute business logic asynchronously. `F-02-javascript-spas_en.pdf`

**Why not static rendering?**  
Static rendering is less suitable for highly interactive or personalized applications such as online banking or games. A trading dashboard has similar personalization and interactivity. `F-02-javascript-spas_en.pdf`

**Trade-off:**  
The initial load may be expensive because the whole application and its resources must be loaded first. But after that, interactions can feel fast.

**Exam sentence:**  
For a highly interactive authenticated dashboard, SPA/CSR is suitable because most UI changes happen in the browser without full page reloads.
# 4. Scenario: “A public service website has simple forms and navigation. It must be reliable even if JavaScript is disabled or fails. No advanced interaction is needed.”

## Which architecture should be chosen❓

**Answer: Server-rendered MPA, or static rendering if the pages are not dynamic.**

If the application only needs normal navigation and forms, a classic MPA is enough. In an MPA, user actions lead to client-server communication and page reloads; the client is a thin client, and most work happens on the server. `F-javascript-architectures-complete.pdf`

For reliability, server-rendered pages are safer than pure CSR because the browser receives ready-made HTML and does not depend heavily on JavaScript to construct the page.

**Why not SPA/CSR?**  
A SPA adds client-side complexity and depends heavily on JavaScript. That is unnecessary when “except navigation, nothing required.”

**Exam sentence:**  
For a simple, reliability-focused site with only navigation and basic forms, server rendering is preferable because the server delivers complete HTML and little client-side JavaScript is required.
# 5. Scenario: “An existing MPA has a search field. The user should see suggestions while typing, but the page should not reload after every letter.”

## Which architecture should be chosen❓

**Answer: MPA + AJAX.**

The lecture uses exactly this kind of example: in a classic MPA, each typed letter could cause a reload, leading to poor user experience, waiting times, network dependence, and difficulty preserving client-side state. AJAX solves this by allowing asynchronous data exchange without reloading the website. `F-javascript-architectures-complete.pdf`

**Process:**

```text
User types letter
→ JavaScript catches keyup event
→ AJAX request asks server for suggestions
→ server returns JSON
→ browser updates DOM locally
→ no full page reload
```

**Exam sentence:**  
Use AJAX inside the MPA because only a small part of the page needs dynamic updates, not the whole application architecture.
# 6. Scenario: “A web app should feel like a desktop application, with immediate reactions, rich UI widgets, and local updates without waiting for a full server response.”

## Which architecture should be chosen❓

**Answer: SPA, or MPA + AJAX for smaller enhancements.**

The lecture says a major challenge is transferring desktop-like features to web applications, such as richer interface components and immediate response to inputs. The prerequisites are data exchange with the server without blocking the interface and local UI updates on the client. `F-javascript-architectures-complete.pdf`

If the whole application is interactive, choose **SPA**. If only one part is interactive, choose **MPA + AJAX**.

**Exam sentence:**  
For a desktop-like experience across the whole application, choose SPA; for a single dynamic widget inside a classic page, use AJAX.
# 7. Scenario: “A Google Docs-like editor should allow long editing sessions, local UI updates, possible offline capability, and no full page reload while working.”

## Which architecture should be chosen❓

**Answer: SPA / CSR.**

The lecture names Google Docs as an SPA example. SPAs aim to provide desktop-like ease of use and response time on the web, use client resources, relieve the server, and can support offline capability. `F-02-javascript-spas_en.pdf`

**Why SPA fits:**

```text
Initial load downloads the app
User edits document
Browser updates UI locally
Server communication happens in background
Page does not reload during use
```

**Trade-off:**  
The client becomes more complex. The lecture lists maintainability, customizability, and client-side complexity as key SPA challenges. `F-02-javascript-spas_en.pdf`

**Exam sentence:**  
A Google Docs-like editor should be an SPA because it needs long interactive sessions and local DOM updates without full page reloads.
# 8. Scenario: “A product detail page must show content very quickly for SEO and user perception, but after loading, users should interact with buttons such as Add to Cart, quantity selector, and reviews without full reloads.”

## Which architecture should be chosen❓

**Answer: SSR / Server-Side Rendering as a hybrid approach.**

SSR combines CSR and server rendering. The server pre-renders the view, sends static HTML, and also sends JavaScript code. The browser first displays the server-rendered view, then JavaScript takes over and boots the SPA through **rehydration**. `F-02-javascript-spas_en.pdf`

**Why this fits:**

```text
Server renders product page HTML
Browser displays product quickly
JavaScript loads
Hydration attaches behavior
Afterwards: Add to Cart works like SPA interaction
```

**Exam sentence:**  
SSR is suitable when the initial page should be visible quickly, but the application should behave like an SPA afterward.
# 9. Scenario: “A pure SPA has poor first load because the browser must download the whole application before showing useful content. What architecture can improve the first visible content❓”

## Which architecture should be chosen❓

**Answer: SSR, or CSR with prerendering depending on the use case.**

SPAs have an expensive initial load because the entire application is loaded first. The lecture says this can be addressed, for example, by SSR. `F-02-javascript-spas_en.pdf`

SSR improves FCP because the initial load contains directly displayable static parts. CSR with prerendering can also make FCP faster than pure CSR because the initial view is pre-generated. `F-02-javascript-spas_en.pdf`

**Choose SSR when:**  
The page should be server-rendered dynamically and then become interactive.

**Choose CSR with prerendering when:**  
The initial view can be statically generated, often for SEO or first display.

**Exam sentence:**  
Use SSR or CSR with prerendering to improve the first visible content of a pure SPA.
# 10. Scenario: “A page looks fully loaded, but none of the buttons work. The team says the page used SSR.”

## What probably failed❓

**Answer: Hydration failed.**

In SSR, the first stage displays server-side pre-rendered HTML. In the second stage, JavaScript “takes over” and boots the SPA through rehydration. If hydration fails, the user may see a fully rendered page that is not interactive. The lecture explicitly mentions this as a worst case. `F-02-javascript-spas_en.pdf`

**Exam sentence:**  
The page is visible because the server-rendered HTML arrived, but it is non-interactive because the JavaScript hydration step failed.
# 11. Scenario: “A landing page must be visible to search engine crawlers, but the main application is still implemented as a SPA.”

## Which architecture should be chosen❓

**Answer: CSR with prerendering, or SSR.**

CSR with prerendering combines CSR and static rendering. Parts required for the initial view are generated during the build process, and it is often used in SEO scenarios to deliver static views to search engine crawlers. `F-02-javascript-spas_en.pdf`

SSR is also possible if the server should dynamically pre-render the page.

**Difference:**

```text
CSR with prerendering:
Initial view generated at build time

SSR:
Initial view generated on the server per request
```

**Exam sentence:**  
For SEO in a SPA, CSR with prerendering is suitable if the initial view can be generated statically; SSR is suitable if the initial view must be generated dynamically.
# 12. Scenario: “An online game has highly interactive personalized state. The content changes constantly during use.”

## Which architecture should NOT be chosen❓

**Answer: Pure static rendering should not be chosen.**

Static rendering is less or not applicable for behavior-driven applications with a high degree of interactivity or personalization, and the lecture gives games as an example. `F-02-javascript-spas_en.pdf`

**Better answer:**  
Use SPA/CSR or another rich client approach, depending on the application. The browser handles frequent UI updates locally, while the server provides data or business logic.

**Exam sentence:**  
Static rendering is unsuitable because the app state is dynamic, personalized, and interaction-heavy.
# 13. Scenario: “A restaurant menu website has only fixed pages: menu, opening hours, address, and gallery. The owner wants the fastest possible delivery and minimal backend complexity.”

## Which architecture should be chosen❓

**Answer: Static rendering.**

The content is stable and not personalized. Static rendering generates complete HTML files during build time and avoids dynamic generation during runtime. This keeps TTFB fast and makes serving simple. `F-02-javascript-spas_en.pdf`

**Exam sentence:**  
Static rendering is best because the pages are content-driven, rarely changing, and can be served as ready-made HTML.
# 14. Scenario: “A shopping website wants every category page to be generated with the newest prices and stock status on every request. The page should work with minimal JavaScript.”

## Which architecture should be chosen❓

**Answer: Server rendering.**

Server rendering creates the view dynamically on demand as soon as a request is received. It is suitable when each request must use current server-side data, such as database access, API calls, or calculations. `F-02-javascript-spas_en.pdf`

**Trade-off:**  
FCP and TTI can be fast because ready-made HTML is delivered, but TTFB may be slower because the server must first render the view and access data. `F-02-javascript-spas_en.pdf`

**Exam sentence:**  
Server rendering is suitable because the page must be generated dynamically with current server-side data.
# 15. Scenario: “A team says: ‘We want a beautiful modern UI.’ Which architecture should we choose❓”

## What is the correct exam answer❓

**Answer: Visual beauty alone does not determine the architecture.**

A visually appealing UI is mainly a matter of HTML, CSS, design, and frontend implementation. Architecture should be chosen based on interaction, rendering, performance, SEO, personalization, reliability, and update frequency.

**If “visually appealing” means rich interactive widgets:**  
Choose SPA or AJAX-enhanced MPA.

**If “visually appealing” just means good layout and styling:**  
MPA, static rendering, server rendering, CSR, or SSR can all be visually appealing.

**Exam sentence:**  
Architecture is not chosen only for visual appeal; it is chosen based on rendering location, interaction level, performance metrics, SEO, and update behavior.
# 16. Scenario: “A website has many pages, but users only click links and read content. There is no need for live updates, filters, offline mode, or complex client-side state.”

## Which architecture should be chosen❓

**Answer: MPA with server rendering, or static rendering if content is stable.**

The lecture defines MPAs as classic web applications based on request-response cycles. User actions lead to client-server communication and reloading of the website. The browser blocks while waiting for the response. `F-javascript-architectures-complete.pdf`

If the pages are dynamic, choose server rendering. If they are stable, choose static rendering.

**Exam sentence:**  
If only navigation is needed, a full SPA is unnecessary; use MPA/server rendering or static rendering.
# 17. Scenario: “A project already uses an MPA, but adding small dynamic features has caused presentation logic and HTML generation to be split between client and server. What architecture problem is this❓”

## What is the answer❓

**Answer: It is an MPA with AJAX, and one downside is fragmented presentation logic.**

AJAX improves user experience and lowers network load, but in MPAs with AJAX, presentation logic and HTML generation can become fragmented between client and server. Also, switching between pages still causes a reload, and the actual application state is still managed on the server. `F-javascript-architectures-complete.pdf`

**Exam sentence:**  
MPA + AJAX improves selected interactions but can split UI logic between browser and server, increasing architectural complexity.
# 18. Scenario: “An application must reduce server work and use the user’s device for more processing. The app is used for long sessions and requires frequent UI updates.”

## Which architecture should be chosen❓

**Answer: SPA / CSR.**

SPAs move classic server tasks to the client. The lecture describes this as a **rich/fat client** approach, where the client takes on more tasks than in classic MPAs, implemented using JavaScript. `F-02-javascript-spas_en.pdf`

**Trade-off:**  
The client becomes more complex, and the first load can be expensive.

**Exam sentence:**  
SPA/CSR is suitable when the client should perform more presentation logic, state management, and UI updates.
# 19. Scenario: “A manager says: ‘Optimize TTFB, FCP, and TTI equally for every page.’ Is this correct❓”

## What is the answer❓

**Answer: No.**

The lecture explicitly says it is not necessary or sensible to optimize all these factors for every application. The architecture depends on what matters most in the scenario. `F-02-javascript-spas_en.pdf`

**Examples:**

```text
Static content site:
Optimize fast TTFB and FCP → static rendering

Highly interactive editor:
Optimize interaction after load → SPA

SEO + SPA interaction:
Optimize FCP and later interactivity → SSR
```

**Exam sentence:**  
Performance metrics must be prioritized according to the application requirements; not every metric has equal importance in every case.
# 20. Scenario: “A site needs fast FCP, fast TTFB, and content is stable. Which rendering approach is best❓”

## Which architecture should be chosen❓

**Answer: Static rendering.**

Static rendering gives fast FCP and TTI like server rendering, and TTFB is also fast because the page does not need to be dynamically generated at request time. `F-02-javascript-spas_en.pdf`

**Exam sentence:**  
When content is stable and fast TTFB/FCP are important, static rendering is usually the best fit.
# Mini exam checklist

When answering architecture scenario questions, write your answer like this:

```text
I would choose [architecture].
Reason 1: It matches the interaction level.
Reason 2: It matches rendering/performance requirements.
Reason 3: It avoids unnecessary complexity.
Trade-off: [mention one disadvantage].
```

Example:

```text
I would choose SSR. The scenario needs a fast initial visible page, but also SPA-like interaction after loading. SSR sends pre-rendered HTML first and then hydrates the page with JavaScript. The trade-off is that hydration can delay interactivity or fail, causing a visible but non-interactive page.
```

## 2. Can the architecture questions be written as real use cases instead of naming the approach ❓

Yes - the **question should describe requirements/use case only**, and the student should infer the architecture. Below are more exam-style questions in that format.

The lecture’s decision logic is mainly based on: page reload behavior, client/server task distribution, asynchronous communication, first load cost, SEO, TTFB/FCP/TTI, personalization, and interactivity. Classic applications reload pages and make the user wait; AJAX avoids reloads for selected interactions; SPAs load the app once and update the DOM; rendering variants decide where/when the final view is created. `F-javascript-architectures-complete.pdf` `F-02-javascript-spas_en.pdf`
# 1. University department website

## Question

A university department wants a website with pages such as:

```text
Home
Study Programs
Professors
Contact
News
```

The pages mostly contain text, images, and links. Content changes only occasionally. The website should load very quickly and should not require complex server processing for every visitor.

## Answer

Choose **static rendering**.

The pages are content-driven and do not change frequently. Therefore, the HTML can be generated before users visit the site. At runtime, the server only sends already existing HTML files.

**Why this fits:**

```text
Content changes rarely
+ mostly reading/navigation
+ fast delivery required
= static rendering
```

**Trade-off:**  
When content changes, a new build and deployment may be needed.
# 2. Public form website with high reliability

## Question

A government website provides forms for address changes, appointments, and information requests. It must work reliably on many browsers, including older ones. JavaScript should not be required for the basic functionality.

## Answer

Choose **server rendering / classic MPA**.

The server can generate complete HTML pages and send them to the browser. Since the browser receives usable HTML, the application does not depend heavily on JavaScript.

**Why this fits:**

```text
Reliability important
+ simple forms
+ broad browser support
+ JavaScript should not be required
= server-rendered MPA
```

**Trade-off:**  
Each major action usually causes a full request-response cycle and page reload.
# 3. Search suggestions in an existing website

## Question

A company already has a normal website. On the product search page, users should see suggestions while typing, like Google search autocomplete. The rest of the website can continue working normally with page reloads.

## Answer

Choose **MPA + AJAX**.

Only one part of the page needs dynamic behavior. Rebuilding the whole application as an SPA would be unnecessary. AJAX allows the browser to ask the server for suggestions in the background and update only the suggestion list.

**Why this fits:**

```text
Existing normal website
+ only one interactive component
+ no reload after every letter
= AJAX enhancement
```

The lecture gives a similar problem: in a classic request-response cycle, every typed letter could cause a page reload, producing poor UX and state-handling problems. AJAX avoids this by exchanging data without reloading the page. `F-javascript-architectures-complete.pdf`
# 4. Google Docs-like editor

## Question

A web application allows users to write and edit documents for a long time. Formatting buttons, cursor movement, typing, comments, and saving should feel immediate. The page should not reload while the user is working.

## Answer

Choose **SPA / client-side rendering**.

The app needs a desktop-like experience. After the initial load, the browser should handle most interactions locally and communicate with the server mainly for data or business logic.

**Why this fits:**

```text
Long interactive session
+ immediate UI updates
+ no full reload while working
+ desktop-like behavior
= SPA / CSR
```

The lecture explicitly uses Google Docs as an SPA example. It also says SPAs aim for desktop-like ease of use and response time. `F-02-javascript-spas_en.pdf`
# 5. Online banking dashboard

## Question

A banking dashboard shows account balances, recent transactions, charts, filters, and personalized user data. It is only visible after login. Search engine visibility is not important.

## Answer

Choose **SPA / client-side rendering**, possibly with API calls.

The page is highly personalized and interaction-heavy. Since SEO is irrelevant behind login, the disadvantages of JavaScript-heavy rendering are less important.

**Why this fits:**

```text
Personalized
+ interactive
+ behind login
+ SEO not important
= SPA / CSR
```

**Trade-off:**  
The initial load may be heavier, and the client-side code becomes more complex.
# 6. News article website

## Question

A news site wants articles to appear very quickly when opened. Search engines should easily understand the article content. Users mostly read articles and click links.

## Answer

Choose **server rendering** if content must be generated dynamically, or **static rendering** if articles can be generated before publication.

A news article is mostly reading content. The browser should receive ready-made HTML quickly.

**Decision detail:**

```text
Articles generated at publishing time → static rendering
Articles assembled dynamically per request → server rendering
```

**Trade-off:**  
Static rendering may require rebuilding or regenerating pages when articles change.
# 7. Product detail page with Add to Cart

## Question

An online shop wants product pages to show product name, image, price, and description immediately. Search engines should read the product content. After loading, users should click “Add to cart”, change quantity, and open reviews without full page reloads.

## Answer

Choose **hybrid server-side rendering / SSR**.

The server first sends visible HTML for fast display and SEO. Then JavaScript takes over and makes the page interactive.

**Why this fits:**

```text
Fast visible product content
+ SEO important
+ later interactive behavior
= SSR
```

**Trade-off:**  
Hydration can add complexity. If hydration fails, the page may look complete but buttons may not work.

SSR works in two stages: first the pre-rendered server view is displayed, then JavaScript takes over and boots the SPA through rehydration. `F-02-javascript-spas_en.pdf`
# 8. Company landing page with animated sections

## Question

A marketing landing page has mostly fixed content: hero section, product features, pricing, testimonials, and contact section. It also has some visual animations, but no complex user state.

## Answer

Choose **static rendering** plus small JavaScript for animation.

The page content is mostly stable. The animations do not require the whole application to become an SPA.

**Why this fits:**

```text
Mostly fixed content
+ fast loading important
+ only visual effects
= static rendering + small JS
```

**Important exam point:**  
“Visually appealing” does not automatically mean SPA. Visual design can be done with HTML/CSS/JavaScript in any architecture.
# 9. Restaurant ordering kiosk

## Question

A restaurant web app lets customers browse menu categories, customize meals, add items to a basket, edit quantities, and place an order. The user should not wait for a full page reload after every small action.

## Answer

Choose **SPA / client-side rendering**.

The basket state, quantity updates, and customization steps are client-side interaction-heavy. Repeated full reloads would harm the user experience.

**Why this fits:**

```text
Many small interactions
+ local basket state
+ no reload after each action
= SPA / CSR
```

**Trade-off:**  
Initial load and client-side complexity are higher.
# 10. Documentation website

## Question

A software project wants documentation pages: installation guide, API guide, tutorials, FAQ, and examples. The content changes when the project releases a new version. Users mostly read and navigate.

## Answer

Choose **static rendering**.

Documentation is usually content-driven and not personalized. The generated files can be served quickly.

**Why this fits:**

```text
Mostly text-based
+ rarely changing
+ reading/navigation
+ fast serving
= static rendering
```

**Trade-off:**  
A new build is needed when documentation changes.
# 11. Weather page with live update button

## Question

A weather website has normal pages, but one section should refresh the current weather when the user clicks “Update”. The whole page should not reload for this small update.

## Answer

Choose **MPA + AJAX**.

The whole page does not need to be an SPA. Only the weather widget needs asynchronous communication.

**Why this fits:**

```text
Normal page
+ one dynamic data section
+ update without full reload
= AJAX
```

AJAX combines DOM manipulation, JavaScript event handling, asynchronous communication, and a data format such as JSON/XML/text. `F-javascript-architectures-complete.pdf`
# 12. Search engine crawler problem

## Question

A public website looks fine in the browser, but search engines do not index the important content well because most content appears only after JavaScript runs.

## Answer

Choose **SSR** or **CSR with prerendering**.

Both can provide directly displayable initial HTML. CSR with prerendering is especially useful when the initial view can be generated ahead of time for crawlers.

**Why this fits:**

```text
Content must be visible to crawlers
+ current JavaScript-heavy page has SEO problem
= SSR or prerendering
```

**Trade-off:**  
SSR adds server/client rendering complexity. Prerendering requires the initial view to be suitable for static generation.
# 13. Game interface in browser

## Question

A browser game has changing game state, player actions, animations, score updates, and personalized progress. Almost everything changes during use.

## Answer

Choose **SPA / client-heavy architecture**, not static rendering.

The application is behavior-driven, highly interactive, and personalized. Static rendering is unsuitable because pages cannot be fully prepared in advance.

**Why this fits:**

```text
Highly interactive
+ constantly changing state
+ personalized progress
= SPA / client-side app
```

The lecture says static rendering is less suitable for behavior-driven applications with high interactivity or personalization, such as online banking or games. `F-02-javascript-spas_en.pdf`
# 14. Simple school timetable website

## Question

A school publishes class timetables as pages. Students only open the page and read the timetable. The timetable changes once per semester.

## Answer

Choose **static rendering**.

The content is stable and read-only. There is no need to dynamically generate the page on every request.

**Why this fits:**

```text
Read-only
+ rarely changing
+ no interaction except navigation
= static rendering
```
# 15. Admin dashboard with filters and tables

## Question

An internal admin dashboard has sortable tables, filters, detail panels, inline editing, charts, and frequent background data loading. It is not public.

## Answer

Choose **SPA / CSR**.

The dashboard is interaction-heavy and not SEO-relevant. The browser can manage UI state, filters, and DOM updates locally.

**Why this fits:**

```text
Internal system
+ many UI states
+ frequent background data loading
+ SEO irrelevant
= SPA / CSR
```

**Trade-off:**  
The client code must be well structured because SPA complexity increases.
# 16. Product catalog with mostly static pages but changing stock count

## Question

A shop catalog has category pages that are mostly stable, but each product card should show current stock availability. The page should load fast, but stock data may be updated after the page appears.

## Answer

Choose **static rendering or server rendering for the base page + AJAX for stock data**.

The base catalog can be delivered quickly. The stock availability can be fetched separately in the background.

**Why this fits:**

```text
Mostly stable page
+ one changing data field
+ fast initial page
= pre-render base + AJAX update
```

**Trade-off:**  
The page may briefly show no stock information or outdated stock until the AJAX response arrives.
# 17. Medical information website

## Question

A hospital publishes health information pages. Users mostly read the content. The site must be reliable, fast, and accessible. There is no need for complex interaction.

## Answer

Choose **static rendering** or **server rendering**.

If content changes rarely, static rendering is ideal. If content is managed dynamically and must always come from a backend CMS at request time, server rendering is also acceptable.

**Why this fits:**

```text
Mostly reading
+ reliability
+ accessibility
+ little interaction
= static/server-rendered HTML
```

**Avoid:**  
A pure JavaScript-heavy app would add unnecessary client-side risk.
# 18. Travel booking flow

## Question

A travel website lets users choose destination, dates, hotel, room type, extras, passenger details, and payment. The process has many steps and the user should not lose entered data while moving between steps.

## Answer

Choose **SPA / CSR**, or possibly **SSR + SPA behavior** if public pages also need SEO.

The booking flow has complex client-side state. An SPA can keep state in the browser and update the view without full reloads.

**Why this fits:**

```text
Multi-step flow
+ lots of temporary user state
+ smooth transitions
= SPA / CSR
```

**Alternative:**  
Use SSR for the public hotel/product pages, then SPA behavior for the booking flow.
# 19. Blog with comment section

## Question

A blog article should load very fast and be readable by search engines. Comments can be loaded after the article appears and added without refreshing the page.

## Answer

Choose **static rendering for the article + AJAX for comments**.

The article is stable content, so static rendering fits. Comments are dynamic, so they can be fetched separately.

**Why this fits:**

```text
Article = stable public content
Comments = dynamic user data
= static article + AJAX comments
```

This is a strong exam answer because it does not force one architecture for the whole page. Different parts can have different needs.
# 20. “Looks complete but buttons do nothing”

## Question

A user opens a page. The product title, price, image, and button are visible immediately. But for a few seconds, clicking the button does nothing. After JavaScript finishes loading, the button starts working.

## Answer

This is likely **SSR with delayed hydration**.

The server-rendered HTML is visible first. The JavaScript has not yet taken over, so the page is not fully interactive. After hydration completes, event handlers are attached and the button works.

**Why this fits:**

```text
Visible first
+ not interactive immediately
+ becomes interactive after JS startup
= SSR hydration behavior
```
# 21. Very low-cost hosting requirement

## Question

A small club wants a website that can be hosted cheaply on a CDN or simple file server. It has pages for events, members, gallery, and contact. There is no login and no personalization.

## Answer

Choose **static rendering**.

Static files can be hosted cheaply and served quickly. No application server is needed for every request.

**Why this fits:**

```text
No login
+ no personalization
+ cheap hosting
+ mostly fixed content
= static rendering
```
# 22. Page must always show personalized recommendations immediately

## Question

An e-commerce homepage must show a logged-in user’s personalized recommendations immediately in the first visible page. The recommendations depend on user history and current promotions.

## Answer

Choose **server rendering** or **SSR**, depending on later interactivity.

If the page only needs normal navigation afterward, server rendering is enough. If it should become SPA-like after loading, choose SSR.

**Why this fits:**

```text
Personalized initial content
+ must be visible immediately
+ depends on backend data
= server-side rendering of initial view
```

**Why not static rendering?**  
The content is user-specific and cannot be generated once for all users.
# 23. Mobile field app with weak network

## Question

Inspectors use a mobile web app in areas with poor internet. They need to open forms, fill checklists, store temporary state locally, and synchronize later.

## Answer

Choose **SPA / CSR**.

The lecture mentions offline capability, especially for mobile use, as one goal of SPAs. The browser can handle more work locally and communicate with the server when available. `F-02-javascript-spas_en.pdf`

**Why this fits:**

```text
Weak network
+ local temporary state
+ later synchronization
= SPA / client-side app
```
# 24. Course registration site during high traffic

## Question

A course registration website has mostly simple pages, but during registration week many students submit forms. The system should avoid unnecessary client complexity, and the server must validate all submissions.

## Answer

Choose **server-rendered MPA**, possibly with small AJAX enhancements.

The core flow is form submission and server validation. Since business correctness matters, the server should remain responsible for validation and response generation.

**Why this fits:**

```text
Simple form flow
+ server-side validation important
+ reliability more important than rich UI
= server-rendered MPA
```
# 25. Interactive map page

## Question

A city transport website has mostly normal information pages, but one page contains an interactive map with zooming, station search, route highlighting, and live data updates.

## Answer

Choose **mixed architecture**: normal pages can be server/static rendered, while the map page behaves like a **client-side interactive app**.

**Why this fits:**

```text
Most pages simple
+ one page highly interactive
= do not make everything SPA unnecessarily
```

For the map page itself, use SPA-like client-side rendering and AJAX/API communication.
# 26. Fast first impression, but later rich app behavior

## Question

A public project management tool wants the landing/dashboard page to show useful information immediately. After the first screen appears, users should navigate between task boards, edit cards, and filter tasks without full page reloads.

## Answer

Choose **SSR**.

The first screen benefits from pre-rendered HTML. After hydration, the application behaves like an SPA.

**Why this fits:**

```text
Fast first visible content
+ later rich interaction
= SSR
```
# 27. Heavy app loaded only once

## Question

A design tool in the browser has a large amount of JavaScript. The first load is slow, but after that users work for hours without navigating away. Most interactions are local.

## Answer

Choose **SPA / CSR**, but acknowledge the initial-load problem.

This app benefits from loading the application once and then using browser resources. The expensive initial load may be acceptable because the session is long.

**Why this fits:**

```text
Heavy initial load
+ long session
+ many local interactions
= SPA / CSR acceptable
```

**Trade-off:**  
First Contentful Paint and Time to Interactive may be worse than simpler architectures.
# 28. “Every metric must be best”

## Question

A client says: “Our application must have the best possible first byte time, first visible content, and interactivity time in every situation.” How should you answer architecturally?

## Answer

You should say that this is not realistic as a single universal choice.

The lecture explicitly says it is not necessary or sensible to optimize all factors for every application. Different applications prioritize different metrics. `F-02-javascript-spas_en.pdf`

**Example answer:**

```text
For mostly static content: optimize TTFB/FCP with static rendering.
For rich interaction: accept heavier initial load and use SPA.
For fast first view plus interaction: use SSR.
```
# 29. Existing page reloads too much

## Question

A website reloads the entire page whenever the user changes a filter in a product list. Users complain because filtering feels slow, but the rest of the website is simple.

## Answer

Choose **AJAX enhancement**.

The filter can send a background request and update the product list in the DOM without reloading the whole page.

**Why this fits:**

```text
Only filtering is slow
+ rest of website simple
+ full rewrite unnecessary
= AJAX
```
# 30. Highly personalized homepage, SEO not important

## Question

After login, each user sees a unique dashboard with notifications, tasks, recommendations, and messages. Public search engines never see this page.

## Answer

Choose **SPA / CSR**.

The page is personalized and interaction-heavy, and SEO is irrelevant. The browser can manage state and update the DOM based on API responses.

**Why this fits:**

```text
Logged-in only
+ personalized
+ many dynamic sections
+ SEO irrelevant
= SPA / CSR
```
# Exam answer pattern

For each scenario, answer like this:

```text
I would choose [architecture].
The reason is that the use case requires [main requirement].
This architecture fits because [technical reason from lecture].
The trade-off is [one disadvantage].
```

Example:

```text
I would choose SSR. The product page must show useful content quickly and be understandable for search engines, but after loading it should behave interactively. SSR sends pre-rendered HTML first and then JavaScript hydrates the page. The trade-off is hydration complexity and possible delay before full interactivity.
```

## 3. Can you give architecture cases for fast maintenance, visual appeal, offline availability, and reliability ❓

Here are **two properly framed architecture scenario questions** where the **question does not reveal the architecture name**.
# 1. Fast, easy maintenance, visually appealing

## Exam-style question

A small design agency wants a public website with the following pages:

```text
Home
Portfolio
Services
About us
Contact
Blog
```

The website should look modern and visually appealing. Most pages contain text, images, animations, and links. The content changes occasionally, but not every minute. The agency has a small technical team, so the solution should be easy to maintain and should not require complex server-side logic for every request. The website should load very fast for visitors.

Which web architecture/rendering approach would you choose? Justify your decision.
## Answer

I would choose **static rendering**.

The reason is that this website is mostly **content-driven**. The pages can be generated before users visit the site. At runtime, the server only sends already prepared HTML, CSS, JavaScript, and image files.

The lecture says that in static rendering, all possible views are pre-generated during the build process, and at runtime static pages are already available on the server as complete HTML files. This means dynamic generation per request is not necessary. Static rendering is suitable for content-driven applications such as blogs and company websites. `F-javascript-architectures-complete.pdf`

### Why it fits this scenario

```text
Fast loading required
+ mostly content pages
+ no complex personalization
+ easy maintenance
+ visually appealing design possible with HTML/CSS
= static rendering
```

### Important clarification

“Visually appealing” does **not** automatically mean SPA. A static website can still look modern using:

```text
HTML
CSS
images
animations
small JavaScript effects
```

The architecture is chosen mainly because the content is stable and the site should be fast and simple.

### Trade-off

If the agency changes content, the site usually needs a new build and deployment. The lecture mentions this as a disadvantage of static rendering. `F-javascript-architectures-complete.pdf`

### Final exam sentence

Static rendering is suitable because the site is content-driven, does not require per-user dynamic generation, and benefits from fast TTFB/FCP while keeping runtime complexity low.
# 2. Offline availability, reliability, slower initial load acceptable

## Exam-style question

A mobile field-work application is used by inspectors in areas with weak internet connection. Inspectors must open checklists, fill forms, add notes, and temporarily keep their work even when the network connection is lost. The application should continue to be usable after it has loaded once. A slower first load is acceptable, because users usually work with the app for a long session after opening it.

Which web architecture/rendering approach would you choose? Justify your decision.
## Answer

I would choose a **Single Page Application with client-side rendering**.

The reason is that the application needs to do a lot of work in the browser after the first load. The lecture says one goal of SPAs is **offline capability**, especially for mobile use. It also says that the initial load loads the complete application and required resources, and afterwards the page is no longer reloaded; the view is updated through DOM manipulation. `F-02-javascript-spas_en.pdf`

### Why it fits this scenario

```text
Offline availability needed
+ weak network
+ long working session
+ local form/checklist state
+ slower initial load acceptable
= SPA / client-side rendering
```

### What happens in practice

```text
1. User opens the app.
2. Browser downloads the application code and resources.
3. Initial load may take longer.
4. After loading, the app can keep forms/checklists active in the browser.
5. User continues working even if the network becomes weak.
6. Data can be synchronized later when the server is reachable.
```

The lecture also notes that the first call of an SPA may be expensive because the entire application is loaded initially. That is acceptable in this scenario because the user works for a long time after the app has started. `F-javascript-architectures-complete.pdf`

### Trade-off

The main disadvantage is that the first load is not as fast as a simple static or server-rendered page. Also, the client-side application becomes more complex and must be carefully designed.

### Final exam sentence

A SPA with client-side rendering is suitable because the application needs offline-capable, long-session interaction in the browser, and the slower initial load is acceptable because the app is loaded once and then used continuously.

## 4. Can you give more architecture use cases with solutions ❓

Below are **more use-case-only exam questions**. The **question describes the situation**, and the **answer identifies the architecture**.

The decision logic comes from the lecture: classic MPAs reload pages and make the user wait; AJAX allows background communication without reloading; SPAs load the app once and then update the DOM; static rendering pre-generates pages; SSR sends pre-rendered HTML first and then JavaScript takes over through hydration. `F-javascript-architectures-complete.pdf` `F-02-javascript-spas_en.pdf`
# 1. Very fast public website, small team, visual design important

## Question

A photography studio wants a public website with a homepage, gallery, pricing, contact page, and a few blog posts. The site must look modern and visually appealing. The team is small and wants simple maintenance. Content changes once or twice per month. Visitors should see the page very quickly.

## Solution

Choose **static rendering**.

The site is mostly content-driven and not personalized. The pages can be generated before users visit them and then served as complete HTML files. This gives fast loading and keeps runtime server complexity low.

**Why:**

```text
Mostly fixed content
+ fast loading
+ easy maintenance
+ visual design possible with HTML/CSS
= static rendering
```

**Trade-off:** content updates usually require a new build/deployment.
# 2. Offline use, reliable after loading, slower first load acceptable

## Question

A mobile inspection app is used in basements and industrial areas with weak internet. Inspectors open the app in the morning, fill many checklists, add comments, and synchronize later. It is acceptable if the first load takes longer, but after that the app should keep working even with poor network.

## Solution

Choose **SPA / client-side rendering**.

The app needs to keep state and behavior in the browser after it has loaded. The lecture lists offline capability, especially for mobile use, as a goal of SPAs. It also says an SPA loads the complete application initially and then updates the view through DOM manipulation without page reloads. `F-02-javascript-spas_en.pdf`

**Why:**

```text
Offline/weak network
+ long working session
+ local form state
+ slower initial load acceptable
= SPA / CSR
```

**Trade-off:** initial load can be expensive, and client-side complexity increases.
# 3. Search suggestions only, rest of website is normal

## Question

An online bookstore has normal pages with full-page navigation. On the search page, when users type into the search box, suggestions should appear immediately. Reloading the whole page after every typed letter would be annoying.

## Solution

Choose **MPA + AJAX**.

Only one part of the page needs dynamic behavior. AJAX lets the browser send a background request, receive suggestion data, and update the DOM without reloading the whole page. The lecture gives this exact type of problem: typing each letter in a classic request-response application would cause reloads and poor UX. `F-javascript-architectures-complete.pdf`

**Why:**

```text
Existing normal website
+ one dynamic widget
+ avoid reload after every key press
= AJAX enhancement
```

**Trade-off:** some presentation logic is now split between server and client.
# 4. Public product page: fast first view + interactive after loading

## Question

An online shop wants product pages to show title, image, price, and description immediately. Search engines should read the product content. After the page appears, users should change quantity, add to cart, open reviews, and switch image previews without full reloads.

## Solution

Choose **SSR / hybrid server-side rendering**.

The first view is generated on the server and sent as HTML, so users and crawlers see content quickly. Then JavaScript takes over and makes the page behave interactively. The lecture describes SSR as a combination of CSR and server rendering where the response contains pre-rendered HTML plus JavaScript, and then rehydration boots the SPA. `F-02-javascript-spas_en.pdf`

**Why:**

```text
Fast visible content
+ SEO important
+ interactive after loading
= SSR
```

**Trade-off:** hydration can be complex; if it fails, the page may look complete but not be interactive.
# 5. Simple government forms, reliability more important than rich UI

## Question

A city website offers appointment booking, address change forms, and downloadable documents. It must work reliably on many devices and should not depend heavily on JavaScript. Users mostly fill a form and submit it.

## Solution

Choose **server-rendered MPA**.

The server generates complete HTML pages. The browser receives a usable page and submits forms through normal request-response cycles. This is suitable when reliability and broad compatibility matter more than desktop-like interaction.

**Why:**

```text
Simple forms
+ broad browser support
+ minimal JavaScript dependency
+ reliability important
= server-rendered MPA
```

**Trade-off:** each major action usually reloads the page.
# 6. Internal admin dashboard with filters, tables, charts

## Question

An internal company dashboard shows tables, filters, charts, expandable rows, inline editing, and notifications. Users stay on the dashboard for long sessions. Search engine visibility is irrelevant because the dashboard is behind login.

## Solution

Choose **SPA / client-side rendering**.

The page is highly interactive and personalized. The browser should manage UI state, filters, table changes, and background data loading. Since SEO is irrelevant, the SEO disadvantage of pure CSR is not a major issue.

**Why:**

```text
Many interactions
+ long session
+ behind login
+ SEO irrelevant
= SPA / CSR
```

**Trade-off:** first load can be heavier, and frontend maintainability becomes important.
# 7. Documentation website, rarely changing content

## Question

A software project needs documentation pages: installation, tutorials, API examples, FAQ, and release notes. Users mainly read and navigate. The documentation changes only when a new version is released.

## Solution

Choose **static rendering**.

Documentation is content-driven and not personalized. The HTML can be generated at build time and served quickly. The lecture says static rendering is suitable for content-driven applications whose content does not change quickly or frequently, such as blogs and company websites. `F-02-javascript-spas_en.pdf`

**Why:**

```text
Mostly text
+ rarely changing
+ fast serving
+ no personalization
= static rendering
```

**Trade-off:** updating documentation requires regeneration/redeployment.
# 8. Live price and stock must be current on first page load

## Question

A shop category page must always show the latest price and stock status immediately when the page opens. The data changes frequently and comes from the backend database. The page itself does not need many advanced interactions.

## Solution

Choose **server rendering**.

The server can load the newest data, generate the HTML dynamically for that request, and send the finished page to the browser. The lecture says server rendering dynamically renders the view on demand when a request is received. `F-02-javascript-spas_en.pdf`

**Why:**

```text
Current backend data required
+ page should be ready immediately
+ little client interaction
= server rendering
```

**Trade-off:** TTFB can be slower because the server must first access data and render the page.
# 9. Mostly static catalog, only stock badge changes

## Question

A product catalog page contains mostly stable content: product name, image, description, and category text. Only the stock badge changes frequently. The company wants the page to appear fast, but stock can be updated shortly after the page appears.

## Solution

Choose **static rendering plus AJAX for stock data**.

The stable page can be pre-generated. The changing stock badge can be fetched in the background after the page loads.

**Why:**

```text
Mostly stable content
+ one small dynamic section
+ fast initial page
= static base page + AJAX update
```

**Trade-off:** the stock badge may appear a little later than the rest of the page.
# 10. Public marketing site with animations

## Question

A startup wants a landing page with hero section, feature cards, pricing, testimonials, smooth scrolling, and animations. There is no login and no personalized content. The page should be easy to host and fast.

## Solution

Choose **static rendering with small JavaScript enhancements**.

Animations and visual effects do not require a full SPA. A visually appealing page can still be static HTML/CSS with some JavaScript.

**Why:**

```text
Public marketing content
+ no personalization
+ visual effects only
+ fast/easy hosting
= static rendering + small JS
```

**Trade-off:** not suitable if the page later becomes a complex interactive application.
# 11. Blog article with dynamic comments

## Question

A blog article should load quickly and be readable by search engines. The comment section can appear after the article loads. Users should post comments without reloading the whole article page.

## Solution

Choose **static rendering or server rendering for the article, plus AJAX for comments**.

The article itself is content, so it should be sent as ready HTML. Comments are dynamic and can be loaded or submitted asynchronously.

**Why:**

```text
Article = stable public content
Comments = dynamic interaction
= rendered article + AJAX comments
```

**Trade-off:** the comment section is partly client-managed.
# 12. Browser-based drawing/design tool

## Question

A design tool runs in the browser. Users draw shapes, move objects, change colors, undo actions, and work for hours. Most operations should happen immediately without waiting for the server. The first load may be large.

## Solution

Choose **SPA / client-side rendering**.

The app behaves like a desktop application. The browser should manage state and interactions locally, while the server is used mainly for saving/loading projects.

**Why:**

```text
Desktop-like tool
+ long session
+ many local interactions
+ large first load acceptable
= SPA / CSR
```

**Trade-off:** client-side architecture must be carefully structured.
# 13. Search engines do not see JavaScript-generated content

## Question

A public website looks fine for users, but search engines do not index important text because the content appears only after JavaScript runs. The initial content is mostly the same for all visitors.

## Solution

Choose **CSR with prerendering** or **SSR**.

If the initial view can be generated ahead of time, use **CSR with prerendering**. If the initial view must be generated per request, use **SSR**. The lecture says CSR with prerendering is often used in SEO to deliver targeted static views for crawlers. `F-02-javascript-spas_en.pdf`

**Why:**

```text
SEO problem
+ content hidden until JavaScript runs
+ initial view should be directly available
= prerendering or SSR
```

**Trade-off:** prerendering requires the initial view to be suitable for static generation.
# 14. Multi-step booking flow with lots of temporary state

## Question

A travel website has a booking process with destination, dates, passengers, hotel options, extras, and payment. Users move back and forth between steps. Entered information should not be lost, and transitions should feel smooth.

## Solution

Choose **SPA / client-side rendering** for the booking flow.

The booking process has lots of temporary client-side state. An SPA can keep that state in the browser and update views without full reloads.

**Why:**

```text
Multi-step process
+ lots of temporary state
+ smooth transitions
+ avoid losing form data
= SPA / CSR
```

**Trade-off:** the implementation is more complex than simple server-rendered forms.
# 15. Basic news website with frequently updated articles

## Question

A news website publishes articles all day. Readers mostly open articles, read them, and click related links. The latest version of an article should be visible when a user opens it.

## Solution

Choose **server rendering**, or **static rendering with frequent rebuilds** if the publishing pipeline supports it.

For a traditional answer, server rendering is safer because the server can generate the page using the latest content on each request.

**Why:**

```text
Content updates frequently
+ users mostly read
+ latest content needed
= server rendering
```

**Trade-off:** TTFB may be slower than static rendering because the server renders dynamically.
# 16. “Looks loaded but buttons do nothing”

## Question

A page opens and immediately shows a todo list and checkboxes. However, for a moment the checkboxes do not react. After JavaScript finishes loading, the checkboxes start working.

## Solution

This indicates **SSR with delayed hydration**.

The server-rendered HTML is visible first. Then JavaScript connects behavior to the existing HTML. Until hydration finishes, the page may be visible but not fully interactive. The lecture warns that a hydration error can lead to an apparently rendered but non-interactive view. `F-02-javascript-spas_en.pdf`

**Why:**

```text
Visible immediately
+ interactive only after JavaScript takes over
= SSR hydration behavior
```
# 17. Small club website, cheapest hosting

## Question

A small sports club needs pages for schedule, team photos, contact, and announcements. There is no login and no personalization. They want cheap hosting and simple maintenance.

## Solution

Choose **static rendering**.

The site can be generated into HTML/CSS/JS files and hosted on a simple web server or CDN.

**Why:**

```text
No login
+ no personalization
+ mostly fixed content
+ cheap hosting
= static rendering
```

**Trade-off:** content updates need rebuilding or regenerating the site.
# 18. Existing MPA feels slow only when filtering

## Question

A product list reloads the entire page whenever the user changes a price filter or category filter. Users complain that filtering feels slow. The rest of the website is simple and acceptable.

## Solution

Choose **AJAX for the filtering part**.

The browser can request filtered data in the background and update only the product list.

**Why:**

```text
Only filtering is slow
+ rest of site is fine
+ full rewrite unnecessary
= AJAX enhancement
```

**Trade-off:** client and server now share responsibility for part of the presentation.
# Quick exam memory rule

```text
Content stable + fast + easy maintenance → static rendering

Dynamic server data + simple pages → server rendering

One dynamic widget inside normal site → AJAX

Long interactive session + local state + offline/weak network → SPA/CSR

Fast first view + later SPA behavior → SSR

SEO problem in JavaScript-heavy app → SSR or prerendering
```

## 5. Why is MPA + AJAX better than a full SPA for search suggestions in a mostly normal website ❓

For this scenario, **MPA + AJAX** is better because the **whole website does not need SPA behavior**. Only **one small component** - the search suggestion box - needs dynamic behavior.

The bookstore already works like this:

```text
Home page → full page load
Book detail page → full page load
Cart page → full page load
Contact page → full page load
```

That is normal **MPA behavior**: user actions usually lead to client-server communication and reloading of the website. The lecture says in MPAs the browser is a **thin client**, and most work such as HTML generation, navigation/routing, and business logic access happens on the server. `F-javascript-architectures-complete.pdf`

But the search box has a special problem:

```text
User types "h"
User types "ha"
User types "har"
User types "harr"
```

If every letter caused a full page reload, the user experience would be bad. The lecture gives exactly this kind of search-suggestion example: every typed letter in a classic request-response application would reload the page, causing waiting time, network dependence, and difficulty remembering the already typed letters. `F-javascript-architectures-complete.pdf`

So we keep the website as an **MPA**, but add **AJAX only for the search suggestions**.

```text
Normal navigation → MPA
Search suggestions → AJAX
```

AJAX is suitable because it enables asynchronous data exchange **without reloading the website**, and the server can provide data through something like a REST API. `F-javascript-architectures-complete.pdf`
# What happens technically❓

```text
1. User opens bookstore page normally.
2. Server sends complete HTML page.
3. User types in search box.
4. JavaScript catches the keyup event.
5. Browser sends AJAX request in the background.
6. Server returns suggestions, usually JSON.
7. JavaScript updates only the suggestion list in the DOM.
8. The full page does not reload.
```

Example:

```text
User types: har
Browser sends: GET /api/suggestions?q=har
Server returns: ["Harry Potter", "Haruki Murakami", "Hardcover notebooks"]
Browser updates only the dropdown list
```

So the page stays normal, but the search box feels modern.
# Why not SPA❓

A **SPA** is useful when the **whole application** should behave like one long-running browser app: no full page reloads, lots of client-side state, many dynamic views, and JavaScript controlling most of the UI.

The lecture says an SPA loads the complete application initially, then the page is no longer reloaded and the view is updated through DOM manipulation. Server communication is mainly for loading data or executing business logic. `F-02-javascript-spas_en.pdf`

That would be too much for this use case.

Here, the bookstore does **not** say:

```text
All navigation should avoid reloads
The cart should be fully client-side
The whole site should behave like an app
Offline mode is needed
Many pages should be dynamically rendered in the browser
```

It only says:

```text
Search suggestions should appear while typing
```

So using a SPA would mean adding a lot of extra complexity for a small requirement. SPAs move many classic server tasks into the client and create a richer/fatter client; the lecture also lists client-side complexity, maintainability, and customizability as SPA challenges. `F-02-javascript-spas_en.pdf`
# Exam-style answer

I would choose **MPA + AJAX**, not a full SPA. The bookstore mainly needs normal page navigation, so an MPA is sufficient for the overall site. Only the search suggestion component needs asynchronous behavior. AJAX solves exactly that problem by sending background requests and updating the DOM without reloading the whole page. A full SPA would be unnecessary because it would move much more responsibility to the client and increase complexity, although the requirement only concerns one dynamic widget.

## 6. Why not use hybrid rendering or SPA when live price and stock must be current on first page load ❓

Good question. **“Immediately” is exactly why pure SPA/CSR is not the best first choice here.** But **hybrid SSR could be acceptable** depending on what happens *after* the page opens.

For the exact scenario you wrote:

> latest price and stock must be shown immediately on first page load  
> data changes frequently  
> comes from backend database  
> page does not need many advanced interactions

the best exam answer is usually **server rendering**.

## Why server rendering fits best

Because the server can do this before sending the page:

```text
1. Browser requests /category/laptops
2. Server asks database for latest prices and stock
3. Server creates complete HTML with that current data
4. Browser receives ready-made HTML
5. User immediately sees latest price and stock
```

That matches the lecture definition: in server rendering, the view is rendered entirely on the server and dynamically on demand as soon as a request is received. `F-javascript-architectures-complete.pdf`

So the first visible page already contains:

```html
<p>Price: 899 €</p>
<p>Stock: 4 available</p>
```

No extra JavaScript startup is needed just to show the correct price.

The trade-off is that **TTFB may be slower**, because the server must first access the database/API and render the page before sending it. But **FCP and TTI can be fast**, because the browser receives ready-made HTML and little client-side JavaScript is needed. `F-javascript-architectures-complete.pdf`
# Why not pure SPA / CSR❓

In pure CSR, the first response often gives the browser the app shell and JavaScript first. The lecture says an SPA’s initial load loads the complete application and required resources, and only afterwards the page is updated via DOM manipulation while server communication loads data or executes business logic. `F-javascript-architectures-complete.pdf`

So the flow would be:

```text
1. Browser requests category page
2. Server sends index.html + JavaScript
3. Browser downloads/runs JavaScript
4. JavaScript requests latest price/stock
5. Server returns JSON
6. Browser updates DOM
7. User finally sees latest price/stock
```

That means the latest price and stock are **not in the first HTML response**. They appear only after JavaScript starts and fetches data.

So for this requirement:

```text
must show latest price and stock immediately on first page load
```

CSR is weaker.

It could show a loading state:

```text
Price: loading...
Stock: loading...
```

but that does **not** satisfy “immediately show latest price and stock.”
# Why not hybrid SSR❓

Actually, **hybrid SSR can also satisfy the “immediate” requirement**, because SSR pre-renders the first view on the server and sends HTML to the browser. The lecture says SSR combines CSR and server rendering: the response contains a pre-rendered view plus additional JavaScript. `F-javascript-architectures-complete.pdf`

So SSR could also do:

```text
Server fetches latest price/stock
Server renders HTML
Browser immediately sees current data
JavaScript hydrates later
```

But in the scenario, the page “does not need many advanced interactions.” That means the SPA part of SSR is unnecessary.

SSR is useful when you need both:

```text
fast first visible server-rendered page
+ rich SPA behavior after loading
```

Your scenario only needs:

```text
fast first visible page
+ current backend data
+ little interaction
```

So plain **server rendering** is simpler and more appropriate.
# Simple decision rule

```text
Need latest backend data immediately,
but little client interaction?
→ Server rendering

Need latest backend data immediately,
and then rich SPA-like interaction?
→ SSR

Need rich interaction,
but first content does not need to be in initial HTML?
→ CSR / SPA
```
# Final exam answer

I would choose **server rendering**, not pure SPA, because the latest price and stock must be included in the first page shown to the user. The server can read the current database values, render the HTML dynamically, and send a ready-made page. A pure SPA would first load JavaScript and then fetch the price/stock data, so the correct values would appear later. Hybrid SSR could also show the data immediately, but it adds SPA hydration complexity; since the page does not need many advanced interactions, plain server rendering is the simpler and more suitable choice.

## 7. Does SPA correspond to CSR, and does MPA correspond to server rendering ❓

Yes - **roughly**, but do not make it a 1:1 rule.

A better way to say it is:

```text
SPA often corresponds to CSR.
MPA often corresponds to server rendering.
```

But there are important exceptions.

## 1. SPA ≈ CSR, but not always

A **SPA** describes the **application behavior**:

```text
The app loads once.
Afterwards, the page is not reloaded.
Views are changed with JavaScript/DOM manipulation.
```

The lecture defines an SPA as an application delivered to the browser that does not reload the page during use, and says that after the initial load, the view is changed via DOM manipulation. `F-02-javascript-spas_en.pdf`

**CSR** describes **where rendering happens**:

```text
The browser builds the view using JavaScript.
```

So, in a normal pure SPA:

```text
SPA behavior + browser builds UI = CSR
```

That is why the lecture says **Client-Side Rendering = SPAs with the advantages and disadvantages already mentioned**. `F-02-javascript-spas_en.pdf`

But a SPA can also be combined with SSR:

```text
Initial page rendered on server
Then JavaScript takes over
After that it behaves like an SPA
```

The lecture calls SSR a hybrid approach: a combination of CSR and server rendering, where the server pre-renders the view and then JavaScript takes over through rehydration. `F-02-javascript-spas_en.pdf`

So:

```text
Pure SPA → usually CSR
SSR app → initially server-rendered, later SPA-like
```
## 2. MPA ≈ server rendering, but not always

An **MPA** describes the **navigation behavior**:

```text
User clicks link.
Browser requests a page.
Server sends a new page.
Browser reloads.
```

The lecture says MPAs work according to the classic request-response cycle, where user actions lead to client-server communication and reloading of the website. `F-javascript-architectures-complete.pdf`

**Server rendering** describes **where rendering happens**:

```text
The server constructs the HTML view.
```

So, in a classic MPA:

```text
MPA behavior + server creates HTML = server rendering
```

That is why the lecture slide says:

```text
Server Rendering = Classic MPAs
```

and explains that the view is rendered entirely on the server, dynamically when the request is received. `F-02-javascript-spas_en.pdf`

But an MPA can also be **static rendered**:

```text
Each page is still a separate page.
Navigation still reloads.
But the HTML was generated earlier during build time.
```

The lecture says static rendering can be realized as MPA as well as SPA. `F-02-javascript-spas_en.pdf`

So:

```text
Classic dynamic MPA → server rendering
Static MPA → static rendering
MPA with small dynamic parts → MPA + AJAX
```
# Best exam mental model

Separate these two questions:

```text
Question 1: How does navigation behave?
→ MPA or SPA

Question 2: Where/when is HTML created?
→ server rendering, static rendering, CSR, SSR, prerendering
```

## Final mapping

```text
MPA
→ usually server rendering
→ can also be static rendering
→ can be enhanced with AJAX

SPA
→ usually CSR
→ can also use SSR
→ can also use prerendering/static rendering for initial views
```

So your intuition is correct, but in exam answers write it carefully:

> **SPA commonly maps to CSR, and classic MPA commonly maps to server rendering, but SPA/MPA describe page behavior, while CSR/server rendering describe where the view is rendered.**

## 8. How can all rendering approaches be identified clearly from examples ❓

A good way to map all approaches is to use **one domain** and ask:

> “For this part of the application, when is the HTML created, who updates the view, and does navigation reload the page?”

Let’s use **one online bookstore** and map every architecture clearly.
# Mental map: Online bookstore

The bookstore has:

```text
Home page
Book detail pages
Search suggestions
Shopping cart
Admin dashboard
Blog/news pages
Public product pages needing SEO
```

Each part can lead to a different architecture.
# 1. Classic MPA / Server Rendering

## Use case

The bookstore has normal pages:

```text
/home
/books/42
/contact
/login
```

When the user clicks a book, a new page loads.

## What happens

```text
User clicks "Book 42"
→ Browser sends GET /books/42
→ Server loads book data from database
→ Server creates complete HTML
→ Browser receives full HTML page
→ Page reloads
```

## How to identify it in exam

Look for these clues:

```text
Full page reload after navigation
Server creates HTML on every request
Current backend/database data needed
Little client-side JavaScript needed
Normal page-based website
```

The lecture says server rendering means **classic MPAs**, where the view is rendered entirely on the server and dynamically on demand when a request is received. `F-02-javascript-spas_en.pdf`

## Why this one❓

Because the browser receives ready-made HTML. It does not need to build the book page using a big JavaScript app.

## Why not SPA❓

Because the requirement does not say the whole bookstore should behave like a desktop app. Normal page navigation is enough.
# 2. Static Rendering

## Use case

The bookstore has stable public pages:

```text
/about
/contact
/help
/blog/how-to-choose-books
```

These pages change rarely.

## What happens

```text
Before users visit:
Markdown/content + template → static site generator → complete HTML files

When user visits:
Browser requests /blog/how-to-choose-books
→ Server sends already existing HTML file
```

## How to identify it in exam

Look for these clues:

```text
Content-driven website
Content changes rarely
Fast loading required
No personalization
No database needed per request
Can rebuild when content changes
```

The lecture says static rendering pre-generates all possible views during the build process; at runtime, complete HTML files already exist, so dynamic generation per request is unnecessary. `F-02-javascript-spas_en.pdf`

## Why this one❓

Because the blog/help pages are stable. Generating them again for every visitor would be unnecessary.

## Why not server rendering❓

Server rendering would work, but it would do extra work on every request. Static rendering is simpler and faster at runtime.
# 3. MPA + AJAX

## Use case

The bookstore is mostly normal page-based, but the search box should show suggestions while typing:

```text
User types: har
Suggestions:
Harry Potter
Haruki Murakami
Hardcover notebooks
```

## What happens

```text
User opens search page normally
→ Server sends full HTML page

User types in search box
→ JavaScript catches keyup event
→ Browser sends background request /api/suggestions?q=har
→ Server returns JSON
→ JavaScript updates only suggestion list
→ Page does not reload
```

## How to identify it in exam

Look for these clues:

```text
Mostly normal website
Only one small part needs dynamic behavior
Background request returns JSON
DOM is updated locally
Navigation between pages still reloads
```

The lecture’s search-suggestion example says that in a classic web app, every typed letter would cause a reload, leading to poor UX and waiting time; AJAX solves this by exchanging data without reloading the website. `F-javascript-architectures-complete.pdf`

## Why this one❓

Because only the search suggestion box needs dynamic behavior.

## Why not SPA❓

Because making the whole bookstore a SPA only for one autocomplete field would add unnecessary client-side complexity.
# 4. SPA / Client-Side Rendering

## Use case

The bookstore has an internal admin dashboard:

```text
Manage books
Edit prices
Filter orders
Sort tables
Open side panels
Drag books into categories
```

The admin works for a long time without wanting full reloads.

## What happens

```text
User opens /admin
→ Server sends index.html + big JavaScript bundle
→ Browser starts the app
→ App requests JSON data
→ Browser builds dashboard UI
→ User filters/sorts/edits
→ JavaScript updates DOM without reload
```

## How to identify it in exam

Look for these clues:

```text
Long interactive session
Many UI states
No full page reloads
Browser manages state
Server mainly provides data/API
SEO not important, often behind login
Initial load may be heavy
```

The lecture says an SPA is delivered to the browser and does not reload the page during use. Its initial load downloads the complete application; afterwards, the view is updated through DOM manipulation and server communication mainly loads data or executes business logic. `F-02-javascript-spas_en.pdf`

## Why this one❓

Because the admin dashboard behaves more like a desktop app than a normal website.

## Why not MPA❓

Full reloads after every filter, edit, or table action would feel slow and would make state management harder.
# 5. Hybrid SSR / Server-Side Rendering with Hydration

## Use case

The bookstore has public book detail pages that need:

```text
Fast first visible content
SEO
Book title, price, image visible immediately
Interactive "Add to cart" button
Image carousel
Review tabs
No reload after interaction
```

## What happens

```text
User opens /books/42
→ Server loads book data
→ Server renders initial HTML
→ Browser immediately shows book title, price, image
→ JavaScript bundle loads
→ Hydration happens
→ Buttons, carousel, tabs become interactive
→ Later actions use background API calls
```

## How to identify it in exam

Look for these clues:

```text
Initial page must be visible quickly
SEO matters
Server sends already visible HTML
Afterwards JavaScript takes over
Page behaves like SPA after loading
Hydration is mentioned or implied
```

The lecture says SSR combines CSR and server rendering. The response contains a pre-rendered view plus additional JavaScript, and then JavaScript “takes over” through rehydration. `F-02-javascript-spas_en.pdf`

## Why this one❓

Because the page needs both:

```text
server-rendered first view
+ SPA-like interaction afterwards
```

## Why not plain server rendering❓

Plain server rendering is enough if the page only needs simple navigation. But here the page should become interactive without reloads.

## Why not pure CSR❓

Pure CSR may show useful content later because the browser first has to download and run JavaScript.
# 6. CSR with Prerendering

## Use case

The bookstore has a public landing page for a campaign:

```text
/summer-reading
```

It is mostly the same for everyone and should be readable by search engines, but after loading it becomes part of the SPA.

## What happens

```text
Build time:
Initial campaign page HTML is pre-generated

Runtime:
Browser receives pre-generated visible HTML
→ JavaScript bundle loads
→ SPA starts
→ Page becomes interactive
```

## How to identify it in exam

Look for these clues:

```text
Initial view can be generated before request
SEO problem in JavaScript-heavy app
Initial static view is enough
Afterwards SPA starts
TTI may be delayed by JavaScript startup
```

The lecture says CSR with prerendering combines CSR and static rendering: parts required for the initial view are generated during the build process, often for SEO, but interactivity is delayed until the SPA starts. `F-02-javascript-spas_en.pdf`

## Why this one❓

Because the first page can be prepared statically, but the app still wants SPA behavior later.

## Why not SSR❓

SSR would dynamically render on each request. That is unnecessary if the initial campaign page is the same for everyone.
# The clearest comparison

| Approach | Bookstore example | How to identify |
|---|---|---|
| **Server Rendering / MPA** | Book detail page with current DB data, simple navigation | Server creates HTML per request; navigation reloads |
| **Static Rendering** | About, help, blog pages | HTML generated at build time; content stable |
| **MPA + AJAX** | Search suggestions while typing | Mostly MPA, but one widget uses background JSON + DOM update |
| **SPA / CSR** | Admin dashboard | App loads once; browser builds views; no reloads |
| **SSR / Hybrid** | Public product page needing SEO + Add to Cart interaction | Server sends visible HTML first; JS hydrates later |
| **CSR with Prerendering** | Static campaign page inside SPA | Initial HTML generated at build time; SPA starts later |
# The most important identification trick

Do not first ask: “Is it SPA or MPA?”

Ask these three questions:

## Question 1: Does navigation reload the page❓

```text
Yes → probably MPA
No → probably SPA
```

## Question 2: When is the first HTML created❓

```text
On every request → server rendering
Before deployment/build time → static rendering or prerendering
In the browser after JS loads → CSR
```

## Question 3: Does JavaScript “take over” already visible HTML❓

```text
Yes → SSR / hydration
No → maybe plain server rendering or static rendering
```
# Very simple memory model

```text
Server Rendering:
"Server cooks the meal when customer orders."

Static Rendering:
"Meals are prepared before customers arrive."

CSR / SPA:
"Customer gets ingredients + recipe; browser cooks the meal."

MPA + AJAX:
"Normal restaurant service, but waiter brings small side items without resetting the table."

SSR:
"Server brings a ready meal first, then JavaScript adds controls and makes it interactive."

CSR with Prerendering:
"A display meal is prepared before opening; JavaScript later turns it into the real interactive app."
```
# Exam-style mini examples

## Example A

“Users only read pages. Content changes once a month. Fast load and easy hosting.”

**Answer:** Static rendering.  
**Why:** Content can be generated before users visit.

## Example B

“Every user must see current stock from the database when the page opens.”

**Answer:** Server rendering.  
**Why:** Server can fetch current data and render HTML per request.

## Example C

“Typing in search should update suggestions without reloading the page.”

**Answer:** MPA + AJAX.  
**Why:** Only one component needs asynchronous update.

## Example D

“Users edit documents for hours, with many local UI changes and possible offline use.”

**Answer:** SPA / CSR.  
**Why:** Browser manages state and updates DOM without reloads.

## Example E

“Public product page must be visible quickly for SEO, but later Add to Cart should work without reload.”

**Answer:** SSR.  
**Why:** Server sends visible HTML first; JavaScript hydrates and makes it interactive.

## Example F

“An SPA has SEO problems, but the first page is the same for all users and can be generated during build.”

**Answer:** CSR with prerendering.  
**Why:** Static initial view helps SEO; SPA starts afterward.
