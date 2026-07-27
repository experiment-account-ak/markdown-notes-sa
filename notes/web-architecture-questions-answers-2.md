# Web Architecture Scenario Questions and Answers

## Question 1

A university department needs a website with Home, About, Contact, Staff, and News pages. The content changes rarely. The site should load very fast and should not require much server processing.

Which architecture should be chosen❓

**Answer:** **Static rendering.**
Because the content changes rarely and requires fast loading with minimal server processing overhead, pre-generating the HTML during the build process is the most efficient choice.

## Question 2

A company blog wants excellent initial load time and SEO. Articles are written by editors and published once or twice per week.

Which architecture should be chosen❓

**Answer:** **Static rendering.**
This architecture provides the extremely fast Time to First Byte (TTFB) and First Contentful Paint (FCP) needed for excellent SEO. Since articles are only published weekly, triggering a new build for content updates is a perfectly acceptable trade-off.

## Question 3

A stock trading dashboard shows constantly changing personalized data. Users interact with charts, filters, and live updates. SEO is irrelevant because the page is behind login.

Which architecture should be chosen❓

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
This is a highly behavior-driven application. Because the data is highly personalized, constantly updating, and hidden behind a login (making SEO irrelevant), a client-heavy approach using asynchronous communication (AJAX/Fetch) is best.

## Question 4

A public service website has simple forms and navigation. It must be reliable even if JavaScript is disabled or fails. No advanced interaction is needed.

Which architecture should be chosen❓

**Answer:** **Server rendering (Classic MPA).**
By generating the complete HTML view directly on the server on demand, the application relies minimally on client-side JavaScript, ensuring excellent reliability and basic functionality even if JavaScript fails.

## Question 5

An existing MPA has a search field. The user should see suggestions while typing, but the page should not reload after every letter.

Which architecture should be chosen❓

**Answer:** **MPA with AJAX.**
Using AJAX (Asynchronous JavaScript and XML) allows the existing application to fetch search suggestions asynchronously in the background and update the DOM locally without requiring a complete architecture overhaul or a full page reload.

## Question 6

A web app should feel like a desktop application, with immediate reactions, rich UI widgets, and local updates without waiting for a full server response.

Which architecture should be chosen❓

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
SPAs are specifically designed to bring desktop-like features to the web. They operate as a rich client, allowing for immediate UI reactions and local updates without synchronous server blocking.

## Question 7

A Google Docs-like editor should allow long editing sessions, local UI updates, possible offline capability, and no full page reload while working.

Which architecture should be chosen❓

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
For a tool requiring long editing sessions and potential offline capability, the browser must act as a fat client. An SPA achieves this by running the application logic directly in the browser.

## Question 8

A product detail page must show content very quickly for SEO and user perception, but after loading, users should interact with buttons such as Add to Cart, quantity selector, and reviews without full reloads.

Which architecture should be chosen❓

**Answer:** **Hybrid Approach: Server-Side Rendering (SSR).**
SSR offers the best of both worlds for e-commerce: it delivers a fully formed, server-rendered static HTML page immediately for SEO and user perception, and then boots up an SPA in the background to handle the complex, reload-free interactions.

## Question 9

A pure SPA has poor first load because the browser must download the whole application before showing useful content. What architecture can improve the first visible content❓

Which architecture should be chosen❓

**Answer:** **Hybrid Approach: CSR with Prerendering** (or **SSR**).
If rewriting the entire application is out of scope, pre-rendering targeted initial views during the build process gives search engine crawlers and users immediate static HTML to look at while the heavy SPA JavaScript downloads in the background.

## Question 10

A page looks fully loaded, but none of the buttons work. The team says the page used SSR.

What probably failed❓

**Answer:** **Rehydration.**
When using Server-Side Rendering (SSR), the server delivers a static HTML view first. The process of the JavaScript code downloading, booting up the SPA, and attaching event listeners to those static buttons is called rehydration. If the page looks ready but doesn't react, rehydration has either lagged or failed entirely.

## Question 11

A landing page must be visible to search engine crawlers, but the main application is still implemented as a SPA.

Which architecture should be chosen❓

**Answer:** **Hybrid Approach: CSR with Prerendering.**
Pre-rendering generates static HTML for specific routes (like the landing page) during the build process so crawlers can easily index it, while the rest of the application functions as a standard Client-Side Rendered SPA.

## Question 12

An online game has highly interactive personalized state. The content changes constantly during use.

Which architecture should NOT be chosen❓

**Answer:** **Static rendering.**
Static rendering relies on pre-generating views at build time. It is completely unsuitable for highly interactive, personalized applications where state and content change constantly during runtime.

## Question 13

A restaurant menu website has only fixed pages: menu, opening hours, address, and gallery. The owner wants the fastest possible delivery and minimal backend complexity.

Which architecture should be chosen❓

**Answer:** **Static rendering.**
Because the content is fixed and the owner wants the fastest possible delivery (Time to First Byte) with minimal backend complexity, pre-building the HTML files is the perfect choice.

## Question 14

A shopping website wants every category page to be generated with the newest prices and stock status on every request. The page should work with minimal JavaScript.

Which architecture should be chosen❓

**Answer:** **Server rendering (Classic MPA).**
Server rendering dynamically generates the HTML on the server the moment the request is made, ensuring absolute real-time data (prices/stock). Delivering a fully formed HTML document means the page works perfectly with minimal or no JavaScript.

## Question 15

A team says: ‘We want a beautiful modern UI.’ Which architecture should we choose❓

What is the correct exam answer❓

**Answer:** **Architecture does not dictate aesthetics.**
The correct exam answer is that "beautiful modern UI" is a matter of CSS, design systems, and frontend frameworks, not the underlying rendering architecture. Any architecture (MPA, SPA, SSR, Static) can have a beautiful, modern UI.

## Question 16

A website has many pages, but users only click links and read content. There is no need for live updates, filters, offline mode, or complex client-side state.

Which architecture should be chosen❓

**Answer:** **Classic Web Application (MPA / Server Rendering or Static Rendering).**
Since there is no need for complex client-side state, live updates, or offline capability, a classic multi-page approach where users simply navigate via links is the most straightforward and appropriate choice.

## Question 17

A project already uses an MPA, but adding small dynamic features has caused presentation logic and HTML generation to be split between client and server. What architecture problem is this❓

What is the answer❓

**Answer:** **Duplication (or scattering) of presentation logic.**
When an MPA is enhanced with ad-hoc AJAX and DOM manipulation, developers often end up writing rendering logic twice: once on the server (e.g., in PHP/Java templates) for the initial load, and once on the client (in JavaScript) for dynamic updates.

## Question 18

An application must reduce server work and use the user’s device for more processing. The app is used for long sessions and requires frequent UI updates.

Which architecture should be chosen❓

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
SPAs act as fat/rich clients. By downloading the application logic to the browser, the user's device handles the processing and UI updates locally, which is ideal for long sessions and drastically reduces server load.

## Question 19

A manager says: ‘Optimize TTFB, FCP, and TTI equally for every page.’ Is this correct❓

What is the answer❓

**Answer:** **No, this is incorrect (Web Architecture is about trade-offs).**
You cannot simultaneously optimize Time to First Byte (TTFB), First Contentful Paint (FCP), and Time to Interactive (TTI) perfectly on every architecture. For example, a pure SPA has excellent subsequent load times but a poor initial FCP; SSR has a great FCP but a delayed TTI due to rehydration.

## Question 20

A site needs fast FCP, fast TTFB, and content is stable. Which rendering approach is best❓

Which architecture should be chosen❓

**Answer:** **Static rendering.**
If the content is stable, generating it at build time and serving it via a CDN guarantees the fastest possible TTFB and FCP.

## Question 21

A university department wants a website with pages such as:

`​`​`text
Home
Study Programs
Professors
Contact
News
`​`​`

The pages mostly contain text, images, and links. Content changes only occasionally. The website should load very quickly and should not require complex server processing for every visitor.

**Answer:** **Static rendering.**
The content (text, images, links) changes only occasionally, and the requirement is extremely fast loading with no complex server processing.

## Question 22

A government website provides forms for address changes, appointments, and information requests. It must work reliably on many browsers, including older ones. JavaScript should not be required for the basic functionality.

**Answer:** **Server rendering (Classic MPA).**
Government sites must be highly accessible. Server rendering builds the forms and responses entirely on the server, ensuring full functionality across all browsers even if JavaScript is disabled or fails to execute.

## Question 23

A company already has a normal website. On the product search page, users should see suggestions while typing, like Google search autocomplete. The rest of the website can continue working normally with page reloads.

**Answer:** **MPA with AJAX.**
The site remains a classic Multi-Page Application, but the specific search input is enhanced with AJAX to fetch suggestions asynchronously without reloading the page.

## Question 24

A web application allows users to write and edit documents for a long time. Formatting buttons, cursor movement, typing, comments, and saving should feel immediate. The page should not reload while the user is working.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
This requires desktop-like interactivity, immediate feedback, and long-lived client state without server interruptions.

## Question 25

A banking dashboard shows account balances, recent transactions, charts, filters, and personalized user data. It is only visible after login. Search engine visibility is not important.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
Because the data is highly personalized, interactive, and completely behind a login wall (making SEO irrelevant), fetching data asynchronously into a client-side shell is optimal.

## Question 26

A news site wants articles to appear very quickly when opened. Search engines should easily understand the article content. Users mostly read articles and click links.

**Answer:** **Static rendering (or Server rendering with heavy caching).**
For a news site where initial load speed and SEO are the absolute top priorities, delivering pre-generated HTML ensures search engines can read it immediately and users see the article instantly.

## Question 27

An online shop wants product pages to show product name, image, price, and description immediately. Search engines should read the product content. After loading, users should click “Add to cart”, change quantity, and open reviews without full page reloads.

**Answer:** **Hybrid Approach: Server-Side Rendering (SSR).**
SSR generates the initial product view on the server for immediate display and SEO indexing. After the initial load, the JavaScript rehydrates the page, turning it into an SPA to handle the cart and reviews without full page reloads.

## Question 28

A marketing landing page has mostly fixed content: hero section, product features, pricing, testimonials, and contact section. It also has some visual animations, but no complex user state.

**Answer:** **Static rendering.**
The content is mostly fixed and visual animations are handled by CSS/JS on the client. Generating this statically provides the best speed and SEO for a marketing page.

## Question 29

A restaurant web app lets customers browse menu categories, customize meals, add items to a basket, edit quantities, and place an order. The user should not wait for a full page reload after every small action.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
The user is navigating a complex flow (customizing meals, managing a cart) that requires constant state updates. Doing this locally in the browser provides a smooth, application-like experience.

## Question 30

A software project wants documentation pages: installation guide, API guide, tutorials, FAQ, and examples. The content changes when the project releases a new version. Users mostly read and navigate.

**Answer:** **Static rendering.**
Documentation is fundamentally stable content that only changes on new releases (which naturally triggers a new build). Static rendering provides fast, easily indexable text pages.

## Question 31

A weather website has normal pages, but one section should refresh the current weather when the user clicks “Update”. The whole page should not reload for this small update.

**Answer:** **MPA with AJAX.**
The website consists of normal pages, but using AJAX allows a specific section (the weather data) to fetch new data asynchronously and update the DOM locally without forcing a full page reload.

## Question 32

A public website looks fine in the browser, but search engines do not index the important content well because most content appears only after JavaScript runs.

**Answer:** **Hybrid Approach: CSR with Prerendering** (or **SSR**).
The current site is suffering from the classic SEO drawback of a pure Single Page Application (CSR), where crawlers see an empty shell. Pre-rendering generates static HTML for those important pages during the build process, feeding search engines immediately readable content while the rest of the site functions as an SPA.

## Question 33

A browser game has changing game state, player actions, animations, score updates, and personalized progress. Almost everything changes during use.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
A browser game requires intense, continuous client-side state changes, user interactions, and screen repaints. The browser must act as a rich client to handle this logic locally without waiting for server network trips.

## Question 34

A school publishes class timetables as pages. Students only open the page and read the timetable. The timetable changes once per semester.

**Answer:** **Static rendering.**
Because the timetable is read-only, the content is identical for everyone, and it changes only once per semester, pre-generating the HTML during the build process guarantees the fastest delivery and lowest server cost.

## Question 35

An internal admin dashboard has sortable tables, filters, detail panels, inline editing, charts, and frequent background data loading. It is not public.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
This requires desktop-level interactivity (sortable tables, inline editing) and frequent background data loading. Since it is hidden behind a login (not public), SEO is irrelevant, making a client-heavy SPA the perfect choice.

## Question 36

A shop catalog has category pages that are mostly stable, but each product card should show current stock availability. The page should load fast, but stock data may be updated after the page appears.

**Answer:** **Static rendering + AJAX.**
The core catalog page (title, images, description) is mostly stable and should be statically rendered for maximum speed and SEO. The volatile stock availability can then be fetched asynchronously via AJAX immediately after the page loads.

## Question 37

A hospital publishes health information pages. Users mostly read the content. The site must be reliable, fast, and accessible. There is no need for complex interaction.

**Answer:** **Static rendering** or **Server rendering (Classic MPA).**
For a purely informational site where reliability and accessibility are paramount and complex interaction is absent, generating full HTML documents (either at build time for Static, or at runtime for Server rendering) ensures the site works perfectly on any device, even with JavaScript disabled.

## Question 38

A travel website lets users choose destination, dates, hotel, room type, extras, passenger details, and payment. The process has many steps and the user should not lose entered data while moving between steps.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
A multi-step booking process requires holding onto a complex user state (dates, rooms, passengers) across multiple views. An SPA handles this seamlessly in the client's memory without losing data during page transitions.

## Question 39

A blog article should load very fast and be readable by search engines. Comments can be loaded after the article appears and added without refreshing the page.

**Answer:** **Static rendering (for the article) with AJAX (for comments).**
The blog article itself is static content that should be pre-built for fast FCP and SEO. The comments section can be injected client-side via AJAX, allowing users to submit new comments without reloading the entire article.

## Question 40

A user opens a page. The product title, price, image, and button are visible immediately. But for a few seconds, clicking the button does nothing. After JavaScript finishes loading, the button starts working.

**Answer:** **Delayed Rehydration (in Server-Side Rendering).**
The site uses SSR, meaning the server delivered the visible HTML immediately. However, the JavaScript required to make the page interactive (booting the SPA and attaching event listeners to the button) is still downloading or executing. This gap between First Contentful Paint and Time to Interactive is the rehydration phase.

## Question 41

A small club wants a website that can be hosted cheaply on a CDN or simple file server. It has pages for events, members, gallery, and contact. There is no login and no personalization.

**Answer:** **Static rendering.**
Static web applications consist purely of HTML, CSS, and JS files generated at build time. They require no application server or database at runtime, meaning they can be hosted very cheaply on a CDN or a basic file server.

## Question 42

An e-commerce homepage must show a logged-in user’s personalized recommendations immediately in the first visible page. The recommendations depend on user history and current promotions.

**Answer:** **Server rendering.**
Because the content must be immediately visible (fast FCP) but is highly personalized to the logged-in user based on real-time data, it cannot be statically pre-built. It must be rendered dynamically on the server at the exact moment of the request.

## Question 43

Inspectors use a mobile web app in areas with poor internet. They need to open forms, fill checklists, store temporary state locally, and synchronize later.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
To function in areas with poor or no internet, the application must operate offline. SPAs transfer the application logic to the client, allowing the device to store temporary state locally and synchronize with the server once the connection is restored.

## Question 44

A course registration website has mostly simple pages, but during registration week many students submit forms. The system should avoid unnecessary client complexity, and the server must validate all submissions.

**Answer:** **Server rendering (Classic MPA).**
When forms require rigorous server-side validation and the site does not need complex client-side interactions, sticking to a classic MPA keeps the architecture simple. The server processes the submissions and returns the result, avoiding unnecessary JavaScript complexity on the client.

## Question 45

A city transport website has mostly normal information pages, but one page contains an interactive map with zooming, station search, route highlighting, and live data updates.

**Answer:** **MPA with a localized SPA (Client-Side Rendering) component.**
The majority of the site operates as a standard, easily accessible MPA. The specific map page leverages Client-Side Rendering (AJAX and DOM manipulation) to handle the complex, real-time interactive requirements without interfering with the architecture of the rest of the site.

## Question 46

A public project management tool wants the landing/dashboard page to show useful information immediately. After the first screen appears, users should navigate between task boards, edit cards, and filter tasks without full page reloads.

**Answer:** **Hybrid Approach: Server-Side Rendering (SSR).**
SSR generates the initial dashboard view on the server so the user sees useful information immediately (fast FCP). Once loaded, the JavaScript rehydrates the page into a full SPA, enabling smooth navigation and interactions without further full page reloads.

## Question 47

A design tool in the browser has a large amount of JavaScript. The first load is slow, but after that users work for hours without navigating away. Most interactions are local.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
Design tools require an enormous amount of client-side logic to function like native desktop apps. The trade-off of a slow initial load (due to downloading large JavaScript bundles) is acceptable because users stay in the application for long, highly interactive sessions.

## Question 48

A client says: “Our application must have the best possible first byte time, first visible content, and interactivity time in every situation.” How should you answer architecturally?

**Answer:** **Web architecture is fundamentally about trade-offs; this request is impossible.**
You must explain that no single architecture excels at everything. A pure SPA has poor initial visibility but excellent interactivity later; Static rendering has perfect initial speed but cannot handle personalized runtime data; SSR has great initial visibility but a delayed time to interactivity (rehydration). The architecture must be chosen based on the application's specific priorities.

## Question 49

A website reloads the entire page whenever the user changes a filter in a product list. Users complain because filtering feels slow, but the rest of the website is simple.

**Answer:** **MPA with AJAX.**
The current setup relies on synchronous server requests for every filter change. By implementing AJAX, the client can send the filter parameters to the server asynchronously and update only the product list in the DOM, eliminating the slow full-page reloads.

## Question 50

After login, each user sees a unique dashboard with notifications, tasks, recommendations, and messages. Public search engines never see this page.

**Answer:** **Single Page Application (SPA) / Client-Side Rendering (CSR).**
Because the dashboard is entirely personalized, requires high interactivity, and is hidden behind a login (meaning SEO is not a factor), a client-rendered SPA that fetches JSON data via an API is the most efficient and scalable approach.

## Question 51

A small design agency wants a public website with the following pages:

`​`​`text
Home
Portfolio
Services
About us
Contact
Blog
`​`​`

The website should look modern and visually appealing. Most pages contain text, images, animations, and links. The content changes occasionally, but not every minute. The agency has a small technical team, so the solution should be easy to maintain and should not require complex server-side logic for every request. The website should load very fast for visitors.

Which web architecture/rendering approach would you choose? Justify your decision.

**Answer:**

**Static rendering.** This is the ideal choice because the content changes rarely, and static files can be served rapidly via a CDN without requiring backend server logic[cite: 1].

## Question 52

A mobile field-work application is used by inspectors in areas with weak internet connection. Inspectors must open checklists, fill forms, add notes, and temporarily keep their work even when the network connection is lost. The application should continue to be usable after it has loaded once. A slower first load is acceptable, because users usually work with the app for a long session after opening it.

Which web architecture/rendering approach would you choose? Justify your decision.

**Answer:**

**Single Page Application (SPA) / Client-Side Rendering (CSR).** The requirement for offline capability and holding complex state over long sessions makes a "rich client" approach essential[cite: 1].

## Question 53

A photography studio wants a public website with a homepage, gallery, pricing, contact page, and a few blog posts. The site must look modern and visually appealing. The team is small and wants simple maintenance. Content changes once or twice per month. Visitors should see the page very quickly.

**Answer:**

**Static rendering.** This provides the fastest load times and ensures the simplest possible maintenance for a small team[cite: 1].

## Question 54

A mobile inspection app is used in basements and industrial areas with weak internet. Inspectors open the app in the morning, fill many checklists, add comments, and synchronize later. It is acceptable if the first load takes longer, but after that the app should keep working even with poor network.

**Answer:**

**Single Page Application (SPA) / Client-Side Rendering (CSR).** Similar to Question 52, the need for offline functionality and continuous operation during long field sessions is best served by a client-side architecture.

## Question 55

An online bookstore has normal pages with full-page navigation. On the search page, when users type into the search box, suggestions should appear immediately. Reloading the whole page after every typed letter would be annoying.

**Answer:**

**MPA with AJAX.** This maintains the classic Multi-Page Application structure while enabling the specific search input to fetch and display suggestions asynchronously without a full reload[cite: 1].

## Question 56

An online shop wants product pages to show title, image, price, and description immediately. Search engines should read the product content. After the page appears, users should change quantity, add to cart, open reviews, and switch image previews without full reloads.

**Answer:**

**Hybrid Approach (SSR).** This provides the necessary initial HTML for SEO while the subsequent "booting" of the SPA handles the cart, reviews, and interactive elements[cite: 1].

## Question 57

A city website offers appointment booking, address change forms, and downloadable documents. It must work reliably on many devices and should not depend heavily on JavaScript. Users mostly fill a form and submit it.

**Answer:**

**Server rendering (Classic MPA).** This ensures maximum compatibility across all devices and browsers, minimizing dependency on client-side JavaScript[cite: 1].

## Question 58

An internal company dashboard shows tables, filters, charts, expandable rows, inline editing, and notifications. Users stay on the dashboard for long sessions. Search engine visibility is irrelevant because the dashboard is behind login.

**Answer:**

**Single Page Application (SPA) / Client-Side Rendering (CSR).** Since SEO is irrelevant, the focus shifts to creating a responsive, rich interface with frequent data updates, which is the strength of an SPA.

## Question 59

A software project needs documentation pages: installation, tutorials, API examples, FAQ, and release notes. Users mainly read and navigate. The documentation changes only when a new version is released.

**Answer:**

**Static rendering.** Documentation is stable content that is perfect for pre-generation at build time, ensuring fast, reliable access for readers.

## Question 60

A shop category page must always show the latest price and stock status immediately when the page opens. The data changes frequently and comes from the backend database. The page itself does not need many advanced interactions.

**Answer:**

**Server rendering (Classic MPA).** Because the data must be fresh from the database on every request and advanced interaction is not required, dynamic server-side generation is the most appropriate approach[cite: 1].

## Question 61

A product catalog page contains mostly stable content: product name, image, description, and category text. Only the stock badge changes frequently. The company wants the page to appear fast, but stock can be updated shortly after the page appears.

**Answer:**

**Static rendering + AJAX.** The stable product information is served statically for speed, while the volatile stock badge is fetched via AJAX immediately after loading.

## Question 62

A startup wants a landing page with hero section, feature cards, pricing, testimonials, smooth scrolling, and animations. There is no login and no personalized content. The page should be easy to host and fast.

**Answer:**

**Static rendering.** For a non-personalized landing page that needs to be fast and cheaply hosted, static generation is the most efficient method[cite: 1].

## Question 63

A blog article should load quickly and be readable by search engines. The comment section can appear after the article loads. Users should post comments without reloading the whole article page.

**Answer:**

**Static rendering + AJAX.** The article is generated statically for SEO and speed, while the comment section is loaded dynamically (asynchronously) to prevent the need for full page refreshes.

## Question 64

A design tool runs in the browser. Users draw shapes, move objects, change colors, undo actions, and work for hours. Most operations should happen immediately without waiting for the server. The first load may be large.

**Answer:**

**Single Page Application (SPA) / Client-Side Rendering (CSR).** Complex design tools require significant client-side logic and immediate feedback, which necessitates an SPA approach.

## Question 65

A public website looks fine for users, but search engines do not index important text because the content appears only after JavaScript runs. The initial content is mostly the same for all visitors.

**Answer:**

**Hybrid Approach (SSR or Prerendering).** The application requires a way to serve "pre-crawled" HTML to the search engine, which SSR or Prerendering provides while keeping the rest of the application as a client-rendered experience.

## Question 66

A travel website has a booking process with destination, dates, passengers, hotel options, extras, and payment. Users move back and forth between steps. Entered information should not be lost, and transitions should feel smooth.

**Answer:**

**Single Page Application (SPA) / Client-Side Rendering (CSR).** A multi-step booking process requires strict state management and smooth transitions that are easiest to handle within an SPA architecture.

## Question 67

A news website publishes articles all day. Readers mostly open articles, read them, and click related links. The latest version of an article should be visible when a user opens it.

**Answer:**

**Server rendering.** To ensure readers see the latest version of an article, the content should be rendered dynamically on the server at the moment of the request[cite: 1].

## Question 68

A page opens and immediately shows a todo list and checkboxes. However, for a moment the checkboxes do not react. After JavaScript finishes loading, the checkboxes start working.

**Answer:**

**Delayed Rehydration (in SSR).** This is a hallmark of Server-Side Rendering where the HTML is delivered fast, but the JavaScript execution (rehydration) lags behind, leaving the page temporarily "dead".

## Question 69

A small sports club needs pages for schedule, team photos, contact, and announcements. There is no login and no personalization. They want cheap hosting and simple maintenance.

**Answer:**

**Static rendering.** This is the most cost-effective and low-maintenance option for a site with fixed, simple content.

## Question 70

A product list reloads the entire page whenever the user changes a price filter or category filter. Users complain that filtering feels slow. The rest of the website is simple and acceptable.

**Answer:**

**MPA with AJAX.** Integrating AJAX allows the filtering to happen asynchronously, keeping the page context and speed while avoiding the performance penalty of a full-page reload[cite: 1].

***

Is there a specific architectural challenge or trade-off in these scenarios that you would like to explore in more detail?
