async function getJSON(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

function tagcount(cardlist, tag) {
    let out = 0;
    for (let card of cardlist) {
        if (card.tags.includes(tag)) {
            out++;
        }
    }
    return out;
}