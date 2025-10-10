# Dainis Zeps Publications - Publication lists
Te sakopojam un grupējam publikācijas pēc tematikas

Here is an overview of my articles, categorized into the following groups:
1) Ancient Languages
2) Combinatorial Mathematics
3) Science and Religion Dialogue
4) Project Russia
5) Emanuel Grinberg's Mathematical Legacy
6) Artificial Intelligence

Each article is assigned to one of these groups. Titles of articles can be extracted and organized by:
- Year
- Topic
- Subject
- Key terms

Searches can also be performed using selected key terms.

Below is a list of platforms where my publications are available:
1) ResearchGate
2) ScirePrints.lu.lv
3) dspace.lu.lv
4) Google Scholar
5) Other platforms that may emerge during ongoing work.


# Combinatorial Mathematics
Organize the following articles under the group Combinatorial Mathematics: 
1) On building 4-critical plane and projective plane multiwheels from odd wheels:​ 
    (wheel graphs, 4-critical graphs, projective plane)
2) Using 2-colorings in the theory of uniquely Hamiltonian graphs: 
    (1H graphs, 2-coloring, Thomassen's conjecture)

Ancient Languages
Organize the following articles under the group Ancient languages: 
1) IN EPISTOLAM AD ROMANOS ANDREAE KNOPKEN COSTERINENSIS​: 
    (epistula ad Romanos, Andreas Knopken)
2) IN LAUDEM NOVAE SCHOLAE: Slavinājums jaunatklājamai skolai​: 
    (Melanchton, Universitas)
3) Aramaicum: Evaņģeliji un psalmi: 
    (Classical Syriac, Biblical Aramaic, Biblical Hebrew, Biblical Greek, LXX)

 Science and Religion Dialogue
Organize the following articles under the group Science and Religion Dialogue: 
1) Ornamental Sign Language In The First Order Tracery Belts​:
    (ornamental belts, sieve shift)
2) The One Savior Paradigm:
    (Christianity, providence, internet)​
3) Cognitum hypothesis and cognitum consciousness: How time and space conception of idealistic philosophy is supported by contemporary physics​:
     (quantum physics, Western philosophy, Peter Uspensky)
4) Four levels of complexity in mathematics and physics​:
    (mathematics, physics, Newton, Berkeley)
5) ΓΝΩΘΙ ΜΑΘΗΜΑ (GNŌTHI MATHĒMA): Vai Kas ir mūsu domāšanas pamati?​
    (ChatGPT, Delfi)
6) Quanta Mathematica Instrumentalis!
    (instrumentalily)
7) Par fiziku: kāpēc daba uzvedas matemātiski? Īss ievadījums kvantu mehānikā:
    (quantum mechanics)
8) Fizika vai Īstenība, kas prevalē?

Project Russia
Organize the following articles under the group Project Russia: 
1) Krievijas Ukrainas karš: saruna ar gpt4o:
    (Ukrainian war, ChatGPT)
2) Vai būt blēdim ir izdevīgi? Ko saka Mākslīgais internets, AI?
    (AI, God, Ethics)
3) Russia's aggressive war against Ukraine: a conversation with gpt.4o and its analysis:
    (Ukrainian war, ChatGPT)
4) Muitnieks un turpnieki:
   (Russia, KGB, Europe)
5) Ius gentium и двадцать первый век или Чтоб земля загорелась под ногами крымнашистов:
    (Ukrainian war, Krimea, ius gentium)
6) On To What In The Contemporary Russia Goes On:
    (Russia, propaganda, FSB, Jedinaja Rossija)
7) Project: Russia:
    (Russia, propaganda, FSB, Jedinaja Rossija)
8) Украинский вопрос:
    (Ukrainian war, Russia, Krimea)
9) Multilingual conversation about war in Ukraine:
    (Ukrainian war, Kievan Rus', ChatGPT)

Emanuel Grinberg's Mathematical Legacy
Organize the following articles under the group Emanuel Grinberg's Mathematical Legacy:
1) ABOUT ONE GEOMETRIC VARIATION PROBLEM. Translation into English:
    (differential geometry, curvature, tensors)
2) The concept of roulette, manuscript:
    (differential geometry)
3) Daži pētījumi par telpas ruletēm:
    (differential geometry, roulettes)
4) The legacy of Emanuels Grinbergs: papers and scientific manuscript facsimiles:
    (Emanuels Grinbergs, differential geometry, graph theory, combinatorics)
5) Par n dimensiju Eiklīda telpas līknēm. Habilitācijas darbs:
    (differential geometry, varieties, osculation spheres)

Artificial Intelligence
Organize the following articles under the group Artificial Intelligence: 
1) GPT no iekšpuses: ko var iesākt ar GPT? Matemātiķa skatījums​:
    (Artificial Intelligence, Large language models, ChatGPT)

### Please, organize database with these group arrangement setting.
- I would like to create a database for my publications divided into thematic groups:
   - Ancient Languages
   - Combinatorial Mathematics
   - Science and Religion Dialogue
   - Project Russia
   - Emanuel Grinberg's Mathematical Legacy
   - Artificial Intelligence
- The database should allow filtering and searching for articles by:
   - Year of publication
   - Theme/Group
   - Subject
   - Keywords (given in brackets beneath titles of articles)
  - Each publication entry should include fields such as:
   - Title
   - Year
 - Group/Category (Ancient Languages, Combinatorial Mathematics, Project Russia, etc.)
   - Keywords
   - Link to the source (e.g., ResearchGate, ScirePrints, Google Scholar)
   - Full-text link or attachment (optional)


async function check(url) {
  try {
    let resp = await fetch(url, { method: 'HEAD' });
    return resp.ok;
  } catch (e) {
    return false;
  }
}

async function makeList() {
  const base = "https://lingua.id.lv/art/war.";
  const max = 80; // var mainīt uz vajadzīgo numuru
  const found = [];

  for (let i = 1; i <= max; i++) {
    let url = base + i + ".pdf";
    let exists = await check(url);
    if (exists) {
      console.log("✅", url);
      found.push(url);
    } else {
      console.log("❌", url);
    }
  }

  // Izvada visu sarakstu vienā blokā
  console.log("---- ATRASTIE FAILI ----");
  found.forEach(f => console.log(f));
}

makeList();

Promise {<pending>}
VM23:19 ✅ https://lingua.id.lv/art/war.1.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.2.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.3.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.4.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.5.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.6.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.7.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.8.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.9.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.10.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.11.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.12.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.12.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.13.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.13.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.14.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.15.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.16.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.17.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.18.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.19.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.20.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.21.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.22.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.23.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.24.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.25.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.26.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.27.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.28.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.29.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.30.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.31.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.32.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.33.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.34.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.35.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.36.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.37.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.38.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.39.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.40.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.41.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.42.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.43.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.44.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.45.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.46.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.47.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.48.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.49.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.49.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.50.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.51.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.52.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.53.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.53.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.54.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.55.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.56.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.57.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.58.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.59.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.60.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.61.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.62.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.63.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.64.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.65.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.66.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.67.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.67.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.68.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.69.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.70.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.70.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.71.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.72.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.73.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.74.pdf
VM23:19 ✅ https://lingua.id.lv/art/war.75.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.76.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.76.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.77.pdf 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.77.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.78.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.78.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.79.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.79.pdf
VM23:3  HEAD https://lingua.id.lv/art/war.80.pdf net::ERR_ABORTED 404 (Not Found)
check @ VM23:3
makeList @ VM23:17
await in makeList
(anonymous) @ VM23:31
VM23:22 ❌ https://lingua.id.lv/art/war.80.pdf
VM23:27 ---- ATRASTIE FAILI ----
VM23:28 https://lingua.id.lv/art/war.1.pdf
VM23:28 https://lingua.id.lv/art/war.2.pdf
VM23:28 https://lingua.id.lv/art/war.3.pdf
VM23:28 https://lingua.id.lv/art/war.4.pdf
VM23:28 https://lingua.id.lv/art/war.5.pdf
VM23:28 https://lingua.id.lv/art/war.6.pdf
VM23:28 https://lingua.id.lv/art/war.7.pdf
VM23:28 https://lingua.id.lv/art/war.8.pdf
VM23:28 https://lingua.id.lv/art/war.9.pdf
VM23:28 https://lingua.id.lv/art/war.10.pdf
VM23:28 https://lingua.id.lv/art/war.11.pdf
VM23:28 https://lingua.id.lv/art/war.14.pdf
VM23:28 https://lingua.id.lv/art/war.15.pdf
VM23:28 https://lingua.id.lv/art/war.16.pdf
VM23:28 https://lingua.id.lv/art/war.17.pdf
VM23:28 https://lingua.id.lv/art/war.18.pdf
VM23:28 https://lingua.id.lv/art/war.19.pdf
VM23:28 https://lingua.id.lv/art/war.20.pdf
VM23:28 https://lingua.id.lv/art/war.21.pdf
VM23:28 https://lingua.id.lv/art/war.22.pdf
VM23:28 https://lingua.id.lv/art/war.23.pdf
VM23:28 https://lingua.id.lv/art/war.24.pdf
VM23:28 https://lingua.id.lv/art/war.25.pdf
VM23:28 https://lingua.id.lv/art/war.26.pdf
VM23:28 https://lingua.id.lv/art/war.27.pdf
VM23:28 https://lingua.id.lv/art/war.28.pdf
VM23:28 https://lingua.id.lv/art/war.29.pdf
VM23:28 https://lingua.id.lv/art/war.30.pdf
VM23:28 https://lingua.id.lv/art/war.31.pdf
VM23:28 https://lingua.id.lv/art/war.32.pdf
VM23:28 https://lingua.id.lv/art/war.33.pdf
VM23:28 https://lingua.id.lv/art/war.34.pdf
VM23:28 https://lingua.id.lv/art/war.35.pdf
VM23:28 https://lingua.id.lv/art/war.36.pdf
VM23:28 https://lingua.id.lv/art/war.37.pdf
VM23:28 https://lingua.id.lv/art/war.38.pdf
VM23:28 https://lingua.id.lv/art/war.39.pdf
VM23:28 https://lingua.id.lv/art/war.40.pdf
VM23:28 https://lingua.id.lv/art/war.41.pdf
VM23:28 https://lingua.id.lv/art/war.42.pdf
VM23:28 https://lingua.id.lv/art/war.43.pdf
VM23:28 https://lingua.id.lv/art/war.44.pdf
VM23:28 https://lingua.id.lv/art/war.45.pdf
VM23:28 https://lingua.id.lv/art/war.46.pdf
VM23:28 https://lingua.id.lv/art/war.47.pdf
VM23:28 https://lingua.id.lv/art/war.48.pdf
VM23:28 https://lingua.id.lv/art/war.50.pdf
VM23:28 https://lingua.id.lv/art/war.51.pdf
VM23:28 https://lingua.id.lv/art/war.52.pdf
VM23:28 https://lingua.id.lv/art/war.54.pdf
VM23:28 https://lingua.id.lv/art/war.55.pdf
VM23:28 https://lingua.id.lv/art/war.56.pdf
VM23:28 https://lingua.id.lv/art/war.57.pdf
VM23:28 https://lingua.id.lv/art/war.58.pdf
VM23:28 https://lingua.id.lv/art/war.59.pdf
VM23:28 https://lingua.id.lv/art/war.60.pdf
VM23:28 https://lingua.id.lv/art/war.61.pdf
VM23:28 https://lingua.id.lv/art/war.62.pdf
VM23:28 https://lingua.id.lv/art/war.63.pdf
VM23:28 https://lingua.id.lv/art/war.64.pdf
VM23:28 https://lingua.id.lv/art/war.65.pdf
VM23:28 https://lingua.id.lv/art/war.66.pdf
VM23:28 https://lingua.id.lv/art/war.68.pdf
VM23:28 https://lingua.id.lv/art/war.69.pdf
VM23:28 https://lingua.id.lv/art/war.71.pdf
VM23:28 https://lingua.id.lv/art/war.72.pdf
VM23:28 https://lingua.id.lv/art/war.73.pdf
VM23:28 https://lingua.id.lv/art/war.74.pdf
VM23:28 https://lingua.id.lv/art/war.75.pdf
found.forEach(url => {
  console.log(`<a href="${url}" target="_blank">${url}</a>`);
});

VM68:1 Uncaught ReferenceError: found is not defined
    at <anonymous>:1:1
(anonymous) @ VM68:1
let raw = `
VM23:28 https://lingua.id.lv/art/war.1.pdf
VM23:28 https://lingua.id.lv/art/war.2.pdf
VM23:28 https://lingua.id.lv/art/war.3.pdf
VM23:28 https://lingua.id.lv/art/war.4.pdf
VM23:28 https://lingua.id.lv/art/war.5.pdf
VM23:28 https://lingua.id.lv/art/war.6.pdf
VM23:28 https://lingua.id.lv/art/war.7.pdf
VM23:28 https://lingua.id.lv/art/war.8.pdf
VM23:28 https://lingua.id.lv/art/war.9.pdf
VM23:28 https://lingua.id.lv/art/war.10.pdf
VM23:28 https://lingua.id.lv/art/war.11.pdf
VM23:28 https://lingua.id.lv/art/war.14.pdf
VM23:28 https://lingua.id.lv/art/war.15.pdf
VM23:28 https://lingua.id.lv/art/war.16.pdf
VM23:28 https://lingua.id.lv/art/war.17.pdf
VM23:28 https://lingua.id.lv/art/war.18.pdf
VM23:28 https://lingua.id.lv/art/war.19.pdf
VM23:28 https://lingua.id.lv/art/war.20.pdf
VM23:28 https://lingua.id.lv/art/war.21.pdf
VM23:28 https://lingua.id.lv/art/war.22.pdf
VM23:28 https://lingua.id.lv/art/war.23.pdf
VM23:28 https://lingua.id.lv/art/war.24.pdf
VM23:28 https://lingua.id.lv/art/war.25.pdf
VM23:28 https://lingua.id.lv/art/war.26.pdf
VM23:28 https://lingua.id.lv/art/war.27.pdf
VM23:28 https://lingua.id.lv/art/war.28.pdf
VM23:28 https://lingua.id.lv/art/war.29.pdf
VM23:28 https://lingua.id.lv/art/war.30.pdf
VM23:28 https://lingua.id.lv/art/war.31.pdf
VM23:28 https://lingua.id.lv/art/war.32.pdf
VM23:28 https://lingua.id.lv/art/war.33.pdf
VM23:28 https://lingua.id.lv/art/war.34.pdf
VM23:28 https://lingua.id.lv/art/war.35.pdf
VM23:28 https://lingua.id.lv/art/war.36.pdf
VM23:28 https://lingua.id.lv/art/war.37.pdf
VM23:28 https://lingua.id.lv/art/war.38.pdf
VM23:28 https://lingua.id.lv/art/war.39.pdf
VM23:28 https://lingua.id.lv/art/war.40.pdf
VM23:28 https://lingua.id.lv/art/war.41.pdf
VM23:28 https://lingua.id.lv/art/war.42.pdf
VM23:28 https://lingua.id.lv/art/war.43.pdf
VM23:28 https://lingua.id.lv/art/war.44.pdf
VM23:28 https://lingua.id.lv/art/war.45.pdf
VM23:28 https://lingua.id.lv/art/war.46.pdf
VM23:28 https://lingua.id.lv/art/war.47.pdf
VM23:28 https://lingua.id.lv/art/war.48.pdf
VM23:28 https://lingua.id.lv/art/war.50.pdf
VM23:28 https://lingua.id.lv/art/war.51.pdf
VM23:28 https://lingua.id.lv/art/war.52.pdf
VM23:28 https://lingua.id.lv/art/war.54.pdf
VM23:28 https://lingua.id.lv/art/war.55.pdf
VM23:28 https://lingua.id.lv/art/war.56.pdf
VM23:28 https://lingua.id.lv/art/war.57.pdf
VM23:28 https://lingua.id.lv/art/war.58.pdf
VM23:28 https://lingua.id.lv/art/war.59.pdf
VM23:28 https://lingua.id.lv/art/war.60.pdf
VM23:28 https://lingua.id.lv/art/war.61.pdf
VM23:28 https://lingua.id.lv/art/war.62.pdf
VM23:28 https://lingua.id.lv/art/war.63.pdf
VM23:28 https://lingua.id.lv/art/war.64.pdf
VM23:28 https://lingua.id.lv/art/war.65.pdf
VM23:28 https://lingua.id.lv/art/war.66.pdf
VM23:28 https://lingua.id.lv/art/war.68.pdf
VM23:28 https://lingua.id.lv/art/war.69.pdf
VM23:28 https://lingua.id.lv/art/war.71.pdf
VM23:28 https://lingua.id.lv/art/war.72.pdf
VM23:28 https://lingua.id.lv/art/war.73.pdf
VM23:28 https://lingua.id.lv/art/war.74.pdf
VM23:28 https://lingua.id.lv/art/war.75.pdf
`;

let links = raw.split('\n').map(line => {
  let match = line.match(/https:\/\/\S+/);
  return match ? match[0] : null;
}).filter(Boolean);

// Izdrukā Markdown formatā
console.log("### Markdown Linku Saraksts:\n");
links.forEach(url => {
  console.log(`- [${url}](${url})`);
});

VM72:79 ### Markdown Linku Saraksts:

VM72:81 - [https://lingua.id.lv/art/war.1.pdf](https://lingua.id.lv/art/war.1.pdf)
VM72:81 - [https://lingua.id.lv/art/war.2.pdf](https://lingua.id.lv/art/war.2.pdf)
VM72:81 - [https://lingua.id.lv/art/war.3.pdf](https://lingua.id.lv/art/war.3.pdf)
VM72:81 - [https://lingua.id.lv/art/war.4.pdf](https://lingua.id.lv/art/war.4.pdf)
VM72:81 - [https://lingua.id.lv/art/war.5.pdf](https://lingua.id.lv/art/war.5.pdf)
VM72:81 - [https://lingua.id.lv/art/war.6.pdf](https://lingua.id.lv/art/war.6.pdf)
VM72:81 - [https://lingua.id.lv/art/war.7.pdf](https://lingua.id.lv/art/war.7.pdf)
VM72:81 - [https://lingua.id.lv/art/war.8.pdf](https://lingua.id.lv/art/war.8.pdf)
VM72:81 - [https://lingua.id.lv/art/war.9.pdf](https://lingua.id.lv/art/war.9.pdf)
VM72:81 - [https://lingua.id.lv/art/war.10.pdf](https://lingua.id.lv/art/war.10.pdf)
VM72:81 - [https://lingua.id.lv/art/war.11.pdf](https://lingua.id.lv/art/war.11.pdf)
VM72:81 - [https://lingua.id.lv/art/war.14.pdf](https://lingua.id.lv/art/war.14.pdf)
VM72:81 - [https://lingua.id.lv/art/war.15.pdf](https://lingua.id.lv/art/war.15.pdf)
VM72:81 - [https://lingua.id.lv/art/war.16.pdf](https://lingua.id.lv/art/war.16.pdf)
VM72:81 - [https://lingua.id.lv/art/war.17.pdf](https://lingua.id.lv/art/war.17.pdf)
VM72:81 - [https://lingua.id.lv/art/war.18.pdf](https://lingua.id.lv/art/war.18.pdf)
VM72:81 - [https://lingua.id.lv/art/war.19.pdf](https://lingua.id.lv/art/war.19.pdf)
VM72:81 - [https://lingua.id.lv/art/war.20.pdf](https://lingua.id.lv/art/war.20.pdf)
VM72:81 - [https://lingua.id.lv/art/war.21.pdf](https://lingua.id.lv/art/war.21.pdf)
VM72:81 - [https://lingua.id.lv/art/war.22.pdf](https://lingua.id.lv/art/war.22.pdf)
VM72:81 - [https://lingua.id.lv/art/war.23.pdf](https://lingua.id.lv/art/war.23.pdf)
VM72:81 - [https://lingua.id.lv/art/war.24.pdf](https://lingua.id.lv/art/war.24.pdf)
VM72:81 - [https://lingua.id.lv/art/war.25.pdf](https://lingua.id.lv/art/war.25.pdf)
VM72:81 - [https://lingua.id.lv/art/war.26.pdf](https://lingua.id.lv/art/war.26.pdf)
VM72:81 - [https://lingua.id.lv/art/war.27.pdf](https://lingua.id.lv/art/war.27.pdf)
VM72:81 - [https://lingua.id.lv/art/war.28.pdf](https://lingua.id.lv/art/war.28.pdf)
VM72:81 - [https://lingua.id.lv/art/war.29.pdf](https://lingua.id.lv/art/war.29.pdf)
VM72:81 - [https://lingua.id.lv/art/war.30.pdf](https://lingua.id.lv/art/war.30.pdf)
VM72:81 - [https://lingua.id.lv/art/war.31.pdf](https://lingua.id.lv/art/war.31.pdf)
VM72:81 - [https://lingua.id.lv/art/war.32.pdf](https://lingua.id.lv/art/war.32.pdf)
VM72:81 - [https://lingua.id.lv/art/war.33.pdf](https://lingua.id.lv/art/war.33.pdf)
VM72:81 - [https://lingua.id.lv/art/war.34.pdf](https://lingua.id.lv/art/war.34.pdf)
VM72:81 - [https://lingua.id.lv/art/war.35.pdf](https://lingua.id.lv/art/war.35.pdf)
VM72:81 - [https://lingua.id.lv/art/war.36.pdf](https://lingua.id.lv/art/war.36.pdf)
VM72:81 - [https://lingua.id.lv/art/war.37.pdf](https://lingua.id.lv/art/war.37.pdf)
VM72:81 - [https://lingua.id.lv/art/war.38.pdf](https://lingua.id.lv/art/war.38.pdf)
VM72:81 - [https://lingua.id.lv/art/war.39.pdf](https://lingua.id.lv/art/war.39.pdf)
VM72:81 - [https://lingua.id.lv/art/war.40.pdf](https://lingua.id.lv/art/war.40.pdf)
VM72:81 - [https://lingua.id.lv/art/war.41.pdf](https://lingua.id.lv/art/war.41.pdf)
VM72:81 - [https://lingua.id.lv/art/war.42.pdf](https://lingua.id.lv/art/war.42.pdf)
VM72:81 - [https://lingua.id.lv/art/war.43.pdf](https://lingua.id.lv/art/war.43.pdf)
VM72:81 - [https://lingua.id.lv/art/war.44.pdf](https://lingua.id.lv/art/war.44.pdf)
VM72:81 - [https://lingua.id.lv/art/war.45.pdf](https://lingua.id.lv/art/war.45.pdf)
VM72:81 - [https://lingua.id.lv/art/war.46.pdf](https://lingua.id.lv/art/war.46.pdf)
VM72:81 - [https://lingua.id.lv/art/war.47.pdf](https://lingua.id.lv/art/war.47.pdf)
VM72:81 - [https://lingua.id.lv/art/war.48.pdf](https://lingua.id.lv/art/war.48.pdf)
VM72:81 - [https://lingua.id.lv/art/war.50.pdf](https://lingua.id.lv/art/war.50.pdf)
VM72:81 - [https://lingua.id.lv/art/war.51.pdf](https://lingua.id.lv/art/war.51.pdf)
VM72:81 - [https://lingua.id.lv/art/war.52.pdf](https://lingua.id.lv/art/war.52.pdf)
VM72:81 - [https://lingua.id.lv/art/war.54.pdf](https://lingua.id.lv/art/war.54.pdf)
VM72:81 - [https://lingua.id.lv/art/war.55.pdf](https://lingua.id.lv/art/war.55.pdf)
VM72:81 - [https://lingua.id.lv/art/war.56.pdf](https://lingua.id.lv/art/war.56.pdf)
VM72:81 - [https://lingua.id.lv/art/war.57.pdf](https://lingua.id.lv/art/war.57.pdf)
VM72:81 - [https://lingua.id.lv/art/war.58.pdf](https://lingua.id.lv/art/war.58.pdf)
VM72:81 - [https://lingua.id.lv/art/war.59.pdf](https://lingua.id.lv/art/war.59.pdf)
VM72:81 - [https://lingua.id.lv/art/war.60.pdf](https://lingua.id.lv/art/war.60.pdf)
VM72:81 - [https://lingua.id.lv/art/war.61.pdf](https://lingua.id.lv/art/war.61.pdf)
VM72:81 - [https://lingua.id.lv/art/war.62.pdf](https://lingua.id.lv/art/war.62.pdf)
VM72:81 - [https://lingua.id.lv/art/war.63.pdf](https://lingua.id.lv/art/war.63.pdf)
VM72:81 - [https://lingua.id.lv/art/war.64.pdf](https://lingua.id.lv/art/war.64.pdf)
VM72:81 - [https://lingua.id.lv/art/war.65.pdf](https://lingua.id.lv/art/war.65.pdf)
VM72:81 - [https://lingua.id.lv/art/war.66.pdf](https://lingua.id.lv/art/war.66.pdf)
VM72:81 - [https://lingua.id.lv/art/war.68.pdf](https://lingua.id.lv/art/war.68.pdf)
VM72:81 - [https://lingua.id.lv/art/war.69.pdf](https://lingua.id.lv/art/war.69.pdf)
VM72:81 - [https://lingua.id.lv/art/war.71.pdf](https://lingua.id.lv/art/war.71.pdf)
VM72:81 - [https://lingua.id.lv/art/war.72.pdf](https://lingua.id.lv/art/war.72.pdf)
VM72:81 - [https://lingua.id.lv/art/war.73.pdf](https://lingua.id.lv/art/war.73.pdf)
VM72:81 - [https://lingua.id.lv/art/war.74.pdf](https://lingua.id.lv/art/war.74.pdf)
VM72:81 - [https://lingua.id.lv/art/war.75.pdf](https://lingua.id.lv/art/war.75.pdf)




### Markdown Linku Saraksts:

   - Nosaukums [https://lingua.id.lv/art/war.1.pdf](https://lingua.id.lv/art/war.1.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.2.pdf](https://lingua.id.lv/art/war.2.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.3.pdf](https://lingua.id.lv/art/war.3.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.4.pdf](https://lingua.id.lv/art/war.4.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.5.pdf](https://lingua.id.lv/art/war.5.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.6.pdf](https://lingua.id.lv/art/war.6.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.7.pdf](https://lingua.id.lv/art/war.7.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.8.pdf](https://lingua.id.lv/art/war.8.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.9.pdf](https://lingua.id.lv/art/war.9.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.10.pdf](https://lingua.id.lv/art/war.10.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.11.pdf](https://lingua.id.lv/art/war.11.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.14.pdf](https://lingua.id.lv/art/war.14.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.15.pdf](https://lingua.id.lv/art/war.15.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.16.pdf](https://lingua.id.lv/art/war.16.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.17.pdf](https://lingua.id.lv/art/war.17.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.18.pdf](https://lingua.id.lv/art/war.18.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.19.pdf](https://lingua.id.lv/art/war.19.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.20.pdf](https://lingua.id.lv/art/war.20.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.21.pdf](https://lingua.id.lv/art/war.21.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.22.pdf](https://lingua.id.lv/art/war.22.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.23.pdf](https://lingua.id.lv/art/war.23.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.24.pdf](https://lingua.id.lv/art/war.24.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.25.pdf](https://lingua.id.lv/art/war.25.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.26.pdf](https://lingua.id.lv/art/war.26.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.27.pdf](https://lingua.id.lv/art/war.27.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.28.pdf](https://lingua.id.lv/art/war.28.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.29.pdf](https://lingua.id.lv/art/war.29.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.30.pdf](https://lingua.id.lv/art/war.30.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.31.pdf](https://lingua.id.lv/art/war.31.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.32.pdf](https://lingua.id.lv/art/war.32.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.33.pdf](https://lingua.id.lv/art/war.33.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.34.pdf](https://lingua.id.lv/art/war.34.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.35.pdf](https://lingua.id.lv/art/war.35.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.36.pdf](https://lingua.id.lv/art/war.36.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.37.pdf](https://lingua.id.lv/art/war.37.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.38.pdf](https://lingua.id.lv/art/war.38.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.39.pdf](https://lingua.id.lv/art/war.39.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.40.pdf](https://lingua.id.lv/art/war.40.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.41.pdf](https://lingua.id.lv/art/war.41.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.42.pdf](https://lingua.id.lv/art/war.42.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.43.pdf](https://lingua.id.lv/art/war.43.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.44.pdf](https://lingua.id.lv/art/war.44.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.45.pdf](https://lingua.id.lv/art/war.45.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.46.pdf](https://lingua.id.lv/art/war.46.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.47.pdf](https://lingua.id.lv/art/war.47.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.48.pdf](https://lingua.id.lv/art/war.48.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.50.pdf](https://lingua.id.lv/art/war.50.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.51.pdf](https://lingua.id.lv/art/war.51.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.52.pdf](https://lingua.id.lv/art/war.52.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.54.pdf](https://lingua.id.lv/art/war.54.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.55.pdf](https://lingua.id.lv/art/war.55.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.56.pdf](https://lingua.id.lv/art/war.56.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.57.pdf](https://lingua.id.lv/art/war.57.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.58.pdf](https://lingua.id.lv/art/war.58.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.59.pdf](https://lingua.id.lv/art/war.59.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.60.pdf](https://lingua.id.lv/art/war.60.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.61.pdf](https://lingua.id.lv/art/war.61.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.62.pdf](https://lingua.id.lv/art/war.62.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.63.pdf](https://lingua.id.lv/art/war.63.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.64.pdf](https://lingua.id.lv/art/war.64.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.65.pdf](https://lingua.id.lv/art/war.65.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.66.pdf](https://lingua.id.lv/art/war.66.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.68.pdf](https://lingua.id.lv/art/war.68.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.69.pdf](https://lingua.id.lv/art/war.69.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.71.pdf](https://lingua.id.lv/art/war.71.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.72.pdf](https://lingua.id.lv/art/war.72.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.73.pdf](https://lingua.id.lv/art/war.73.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.74.pdf](https://lingua.id.lv/art/war.74.pdf)
   - Nosaukums [https://lingua.id.lv/art/war.75.pdf](https://lingua.id.lv/art/war.75.pdf)
