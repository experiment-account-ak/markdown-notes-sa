[Source chat](https://chatgpt.com/g/g-p-6a295be0712c8191a00e1149bb7206ea-software-architecture-exam-preparation/c/6a49062c-bafc-83eb-ad19-b118011f3599)

# F-02: Single Page Applications - mental model

A **Single Page Application (SPA)** is best understood as:

> **A web app that is downloaded once, then behaves more like a desktop app inside the browser.**

In a classic website, every major user action often asks the server for a **new HTML page**. In an SPA, the browser first downloads the app, usually one HTML page plus lots of JavaScript/CSS/images. After that, the page is **not reloaded**. Instead, JavaScript changes the visible page by manipulating the **DOM**, and the server is contacted mainly for **data** or **business logic**, often asynchronously via AJAX. This is the central idea of the lecture. `F-02-javascript-spas_en.pdf`

# 1. What is an SPA?

The lecture defines an SPA as an application delivered to the browser that **does not reload the page during use**. `F-02-javascript-spas_en.pdf`

Think of it like this:

| Classic MPA | SPA |
|---|---|
| User clicks → browser asks server → server sends a new HTML page | User clicks → JavaScript reacts → browser updates only part of the page |
| Server prepares most views | Browser prepares/updates most views |
| More page reloads | No full page reload during normal use |

A simple example is **Google Docs**. When you type in a document, the whole page does not reload. The browser updates the document area, toolbar state, cursor position, etc., while background communication with the server saves or syncs data.

# 2. Why do SPAs exist?

The lecture gives three main goals:

1. **Desktop-like ease of use and response time**  
   Example: editing a document, opening menus, selecting text, or formatting text should feel fast, like a desktop office application.

2. **Use client resources and relieve the server**  
   The browser can do more work: rendering, state management, interface logic. This can reduce server load and help with scaling and cost.

3. **Offline capability, especially for mobile use**  
   Since much of the application is already on the client, parts of the app may continue working without constant server communication. `F-02-javascript-spas_en.pdf`


# 3. SPA request flow: what happens step by step?

The diagrams on pages 4-6 show the core SPA flow.

## Initial load

The user opens something like:

```text
/index.html
```

The browser sends an HTTP request to the server. The server sends back the SPA application: usually one HTML file plus JavaScript, CSS, images, and other resources.

Then the browser renders the initial page.

## Later user interaction

After the app is loaded, the user does something, for example types into a search field. The browser does **not** reload the whole page. Instead:

1. JavaScript handles the event, such as `onkeyup`.
2. JavaScript sends a background HTTP request.
3. The server returns data, often JSON.
4. JavaScript updates the DOM.
5. The visible HTML changes without a full page reload.

The key idea is: **the page stays alive; only parts of it change.**

### PlantUML sequence diagram

> **IMAGE PLACEHOLDER:** SPA request flow sequence diagram


# 4. Exam question: What are the main features of an SPA?

The lecture lists three important SPA features:

1. **The initial load loads the complete application including required resources.**

   This means the first request can be heavier because the browser receives the JavaScript application.

2. **Afterwards, the page is no longer reloaded.**

   The app changes the view by DOM manipulation.

3. **Server communication only happens to load data or execute business logic.**

   Example: a todo app may already have the UI in the browser, but it asks the server for the todo list data. `F-02-javascript-spas_en.pdf`


# 5. MPA vs SPA: distribution of tasks

The diagram on page 9 compares **MPA** and **SPA** task distribution.

In an **MPA**, the browser mostly renders HTML. The server does more work:

- presentation logic,
- HTML generation,
- state management,
- business logic,
- authentication,
- authorization.

In an **SPA**, many tasks move to the client:

- HTML rendering,
- presentation logic,
- HTML generation,
- state management,
- sometimes business logic.

The server still commonly keeps important backend responsibilities:

- business logic,
- authentication,
- authorization,
- database access,
- access to external services.

This is why the lecture says SPAs use a **rich client** or **fat client**. The browser is no longer just a passive HTML display tool; it becomes an active application runtime. `F-02-javascript-spas_en.pdf`

### PlantUML component diagram

> **IMAGE PLACEHOLDER:** MPA vs SPA task distribution component diagram


# 6. Important term: Rich client / fat client

A **rich client** means the client does more than just display HTML.

In an SPA, the browser may handle:

- page transitions,
- button behavior,
- state such as selected todo/filter/user input,
- rendering lists and details,
- validation before sending data,
- temporary offline state.

Older terminology for such applications is **Rich Internet Application**, or **RIA**. The lecture says SPAs implement the client part using JavaScript. `F-02-javascript-spas_en.pdf`


# 7. Key challenges of SPAs

SPAs solve some user-experience problems, but they create new complexity in the browser.

The lecture highlights these challenges:

## Client-side complexity

Because many server-side tasks move to JavaScript, the client becomes harder to maintain and customize.

Possible solutions mentioned:

- design principles,
- architectural patterns,
- frameworks.

This is why frameworks like React, Angular, and Vue.js become relevant later.

## Browser functions

Initially, SPAs had problems with native browser functions such as:

- back button,
- forward button,
- bookmarks.

These are now largely solved using **routers**.

A router makes the SPA understand URLs such as:

```text
/todos
/todos/42
/settings
```

Even though the browser is still inside one application, the router decides which view to show.

## Expensive initial load

Because the whole application may be downloaded initially, the first load can be expensive.

## SEO problems

Search engines may have difficulty with JavaScript-heavy applications if they cannot properly execute and understand the client-rendered content.

## JavaScript itself

The lecture humorously lists JavaScript as a challenge. The point is that larger JavaScript applications can become complex and need structure. `F-02-javascript-spas_en.pdf`


# 8. Exam question: Why is a pure SPA not always the right choice?

A pure SPA uses **client-side rendering**: the browser receives a minimal page plus JavaScript, then JavaScript builds the UI.

This is not always ideal because:

- the initial load may be large,
- SEO may be harder,
- the user may wait before seeing useful content,
- the app may become complex on the client,
- some applications do not need such interactivity.

So the lecture introduces **architectural variants**. The central question becomes:

> **Where and when is the view rendered?**

That means: is the final HTML constructed on the server, during build time, in the browser, or through a combination? `F-02-javascript-spas_en.pdf`


# 9. Performance metrics: TTFB, FCP, TTI

The lecture introduces three important metrics.

| Metric | Meaning | Simple explanation |
|---|---|---|
| **TTFB** | Time to First Byte | How long until the browser receives the first byte from the server |
| **FCP** | First Contentful Paint | How long until the user sees first useful content, such as text or graphics |
| **TTI** | Time to Interactive | How long until the page is usable, for example buttons and links work |

Important lecture warning: it is **not necessary or sensible to optimize all metrics for every application**. Different apps need different priorities. `F-02-javascript-spas_en.pdf`

Example:

A blog should probably optimize fast visible content and SEO.

An online editor may care more about interactivity after loading.


# 10. Rendering approaches

The lecture discusses four main rendering approaches:

1. **Server rendering**
2. **Static rendering**
3. **Client-side rendering**
4. **Hybrid approaches**
   - server-side rendering,
   - CSR with prerendering.


# 11. Server rendering

Server rendering is the classic MPA style.

The view is rendered completely on the server. When a request arrives, the server dynamically creates the HTML and sends it to the browser.

Example technologies from the lecture:

- Spring MVC with Thymeleaf,
- Ruby on Rails,
- PHP.

## Evaluation

Advantage:

- **FCP and TTI are fast**, because ready-made HTML is delivered and little client-side JavaScript is needed.

Disadvantage:

- **TTFB can be slow**, because the server must first render the page. This may involve database access, API calls, and calculations. `F-02-javascript-spas_en.pdf`

### Simple flow

> **IMAGE PLACEHOLDER:** Server rendering simple flow diagram


# 12. Static rendering

Static rendering means:

> All possible views are pre-generated during the build process.

At runtime, the server already has complete HTML files. It does not need to dynamically generate the page for every request.

The lecture says static rendering can be used with both MPA and SPA approaches. It is also a basis for architectures such as **Jamstack**.

Example technologies:

- Gatsby,
- Jekyll,
- Hugo,
- Next.js.

## Evaluation

Advantages:

- **FCP and TTI are fast**, as long as not too much client-side JavaScript is involved.
- **TTFB is fast**, because the server does not need to dynamically generate the page.

Disadvantages:

- Good for content-driven apps like blogs or company websites.
- Less suitable for highly interactive or personalized apps such as online banking or games.
- Updating content requires a new build and deployment. `F-02-javascript-spas_en.pdf`


# 13. Client-side rendering

Client-side rendering, or **CSR**, is the typical pure SPA approach.

The server sends the app shell and JavaScript. The browser then uses JavaScript to build the view.

Example technologies:

- React,
- Angular,
- Vue.js.

## Main idea

The server does not send the final full HTML view. The browser builds the view after downloading and executing JavaScript.

### CSR flow

> **IMAGE PLACEHOLDER:** Client-side rendering flow diagram

CSR has the SPA advantages already discussed, but also the initial-load and SEO challenges. `F-02-javascript-spas_en.pdf`


# 14. Hybrid approach: Server-Side Rendering

Server-Side Rendering, or **SSR**, combines CSR and server rendering. The lecture also calls this **Universal Rendering**.

In SSR:

1. The server pre-renders the view as static HTML.
2. The response also contains JavaScript code.
3. The browser immediately displays the pre-rendered HTML.
4. Then JavaScript “takes over” and boots the SPA.
5. This takeover process is called **rehydration**.

Example technologies:

- Next.js for React,
- Nuxt.js for Vue,
- built-in tools in Angular, React, and Vue ecosystems. `F-02-javascript-spas_en.pdf`

## Rehydration explained simply

Imagine the server sends a printed form. The user can already see the form. But the form is not “alive” yet.

Then JavaScript loads and attaches behavior:

- buttons become clickable,
- checkboxes get event handlers,
- navigation becomes SPA navigation,
- state becomes managed by JavaScript.

That process is **rehydration**.


# 15. Code used in the lecture: SSR example

This is the important code example from the SSR section.

```html
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <title>My Todos</title>
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <h1>My Todos</h1>
    <ul>
      <li><input type="checkbox"> Learn JavaScript</li>
      <li><input type="checkbox"> Check GraphQL</li>
    </ul>
    <script>
      var DATA = { "todos": [
        { "text": "Lorem ipsum...", "title": "Learn JavaScript", "id": "42" },
        { "text": "Dolor sit amet...", "title": "Check GraphQL", "id": "23" }
      ]};
    </script>
    <script src="/bundle.js"></script>
  </body>
</html>
```

## What each part means

```html
<!DOCTYPE html>
<html lang="de">
```

This declares an HTML document. The language is German, shown by `lang="de"`.

```html
<head>
  <meta charset="utf-8">
  <title>My Todos</title>
  <link rel="stylesheet" href="/style.css" />
</head>
```

This is metadata and styling:

- `utf-8` defines character encoding.
- `<title>` sets the browser tab title.
- `<link rel="stylesheet">` loads CSS.

```html
<h1>My Todos</h1>
<ul>
  <li><input type="checkbox"> Learn JavaScript</li>
  <li><input type="checkbox"> Check GraphQL</li>
</ul>
```

This is the **server-side pre-rendered static HTML**. It can be displayed immediately, before the SPA is fully active.

This improves **FCP**, because the user sees content quickly.

```html
<script>
  var DATA = { "todos": [
    { "text": "Lorem ipsum...", "title": "Learn JavaScript", "id": "42" },
    { "text": "Dolor sit amet...", "title": "Check GraphQL", "id": "23" }
  ]};
</script>
```

This embeds the data needed by the SPA.

Why is this useful?

The HTML already displays the todos, but the JavaScript application also needs the same data when it starts. Without this embedded data, the SPA might need to request the same data again.

```html
<script src="/bundle.js"></script>
```

This loads the SPA JavaScript bundle.

The bundle performs **rehydration**: it attaches JavaScript behavior to the already visible HTML.

## SSR evaluation

Advantages:

- **FCP is faster than pure CSR**, because the initial response already contains displayable HTML.

Challenges:

- The rendering code must work on both server and client. This is why SSR is also called **isomorphic rendering**.
- TTFB and TTI depend heavily on implementation quality.
- Worst case: rehydration fails, and the page looks complete but is not interactive. `F-02-javascript-spas_en.pdf`


# 16. Hybrid approach: CSR with prerendering

CSR with prerendering combines:

- client-side rendering,
- static rendering.

Parts required for the initial view are generated during the build process.

This is often useful for SEO because search engines can receive a static initial page.

Example technologies from the lecture:

- prerenderer library,
- Prerender.io.

## Evaluation

Advantages:

- **FCP is faster than pure CSR**, because the initial load contains displayable static parts.
- **TTFB is similar to CSR**, usually fast except for the initial load.

Disadvantages:

- **TTI is delayed**, because the SPA still needs to start up.
- The initial view must be suitable for static rendering. This can be difficult if the content is highly personalized or changes very often. `F-02-javascript-spas_en.pdf`


# 17. Rendering approaches comparison

| Approach | Where is HTML created? | When is it created? | Good for | Main risk |
|---|---|---|---|---|
| **Server rendering** | Server | On each request | Classic dynamic websites | TTFB can be slow |
| **Static rendering** | Build system/server output | Before runtime, during build | Blogs, company sites, content pages | Content updates need rebuild |
| **CSR** | Browser | After JavaScript loads | Highly interactive SPAs | Slow first useful view, SEO issues |
| **SSR** | Server first, browser later | Request time + browser hydration | SPAs needing faster first display | Hydration complexity |
| **CSR with prerendering** | Build first, browser later | Build time + browser startup | SEO/static initial pages | TTI delayed, initial view must be static |


# 18. Big mental map of the lecture

> **IMAGE PLACEHOLDER:** SPA lecture mental map


# 19. Exam-style questions to prepare

## What is a Single Page Application?

An SPA is a browser-delivered application that does not reload the page during normal use. It updates the view using JavaScript and DOM manipulation.

## What happens during the initial load of an SPA?

The browser downloads the application resources: HTML, JavaScript, CSS, images, and other required files.

## What happens after the initial load?

The browser handles user actions with JavaScript, communicates with the server mainly for data or business logic, and updates the DOM without reloading the page.

## Why is the SPA client called a rich or fat client?

Because many tasks that were traditionally done on the server move to the browser, such as presentation logic, HTML generation, and state management.

## What are TTFB, FCP, and TTI?

TTFB measures when the first response byte arrives. FCP measures when the first content appears. TTI measures when the page becomes interactive.

## What is the difference between CSR and SSR?

CSR renders the view in the browser after JavaScript loads. SSR pre-renders the initial view on the server, sends HTML to the browser, and then JavaScript rehydrates it.

## What is rehydration?

Rehydration is the process where JavaScript takes over server-rendered HTML and makes it interactive.

## Why can SSR be risky?

If rehydration fails, the page may look complete but not respond to user interaction.


# 20. Final one-sentence summary

An **SPA** moves much of the application behavior into the browser: the app is loaded once, later interactions update the DOM without full reloads, and different rendering strategies such as CSR, SSR, static rendering, and prerendering exist to balance speed, interactivity, SEO, and complexity.

