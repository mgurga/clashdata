// let saved_deck = [];

document.querySelector("#commondeckdropdown").onchange = function() {
    const deckname = document.querySelector("#commondeckdropdown").value;
    const chs = document.querySelectorAll(".cardholder");

    if (deckname == "blank") {
        // TODO: Save current deck then switch to selected common deck
    } else if (deckname == "26hog") {
        chs[0].innerHTML = `<img src="/static/cards/26000021.png" class="cardimg" draggable="true" id="26000021">`;
        chs[1].innerHTML = `<img src="/static/cards/26000038.png" class="cardimg" draggable="true" id="26000038">`;
        chs[2].innerHTML = `<img src="/static/cards/26000014.png" class="cardimg" draggable="true" id="26000014">`;
        chs[3].innerHTML = `<img src="/static/cards/28000000.png" class="cardimg" draggable="true" id="28000000">`;
        chs[4].innerHTML = `<img src="/static/cards/28000011.png" class="cardimg" draggable="true" id="28000011">`;
        chs[5].innerHTML = `<img src="/static/cards/26000030.png" class="cardimg" draggable="true" id="26000030">`;
        chs[6].innerHTML = `<img src="/static/cards/26000010.png" class="cardimg" draggable="true" id="26000010">`;
        chs[7].innerHTML = `<img src="/static/cards/27000000.png" class="cardimg" draggable="true" id="27000000">`;
    } else if (deckname == "lumberloon") {
        chs[0].innerHTML = `<img src="/static/cards/26000006.png" class="cardimg" draggable="true" id="26000006">`;
        chs[1].innerHTML = `<img src="/static/cards/26000035.png" class="cardimg" draggable="true" id="26000035">`;
        chs[2].innerHTML = `<img src="/static/cards/26000000.png" class="cardimg" draggable="true" id="26000000">`;
        chs[3].innerHTML = `<img src="/static/cards/26000049.png" class="cardimg" draggable="true" id="26000049">`;
        chs[4].innerHTML = `<img src="/static/cards/26000064.png" class="cardimg" draggable="true" id="26000064">`;
        chs[5].innerHTML = `<img src="/static/cards/26000030.png" class="cardimg" draggable="true" id="26000030">`;
        chs[6].innerHTML = `<img src="/static/cards/28000011.png" class="cardimg" draggable="true" id="28000011">`;
        chs[7].innerHTML = `<img src="/static/cards/28000017.png" class="cardimg" draggable="true" id="28000017">`;
    } else if (deckname == "logbait") {
        chs[0].innerHTML = `<img src="/static/cards/28000004.png" class="cardimg" draggable="true" id="28000004">`;
        chs[1].innerHTML = `<img src="/static/cards/26000000.png" class="cardimg" draggable="true" id="26000000">`;
        chs[2].innerHTML = `<img src="/static/cards/27000003.png" class="cardimg" draggable="true" id="27000003">`;
        chs[3].innerHTML = `<img src="/static/cards/28000003.png" class="cardimg" draggable="true" id="28000003">`;
        chs[4].innerHTML = `<img src="/static/cards/26000026.png" class="cardimg" draggable="true" id="26000026">`;
        chs[5].innerHTML = `<img src="/static/cards/26000030.png" class="cardimg" draggable="true" id="26000030">`;
        chs[6].innerHTML = `<img src="/static/cards/26000010.png" class="cardimg" draggable="true" id="26000010">`;
        chs[7].innerHTML = `<img src="/static/cards/28000011.png" class="cardimg" draggable="true" id="28000011">`;
    } else if (deckname == "xbow") {
        chs[0].innerHTML = `<img src="/static/cards/27000008.png" class="cardimg" draggable="true" id="27000008">`;
        chs[1].innerHTML = `<img src="/static/cards/27000006.png" class="cardimg" draggable="true" id="27000006">`;
        chs[2].innerHTML = `<img src="/static/cards/28000000.png" class="cardimg" draggable="true" id="28000000">`;
        chs[3].innerHTML = `<img src="/static/cards/26000010.png" class="cardimg" draggable="true" id="26000010">`;
        chs[4].innerHTML = `<img src="/static/cards/26000000.png" class="cardimg" draggable="true" id="26000000">`;
        chs[5].innerHTML = `<img src="/static/cards/26000030.png" class="cardimg" draggable="true" id="26000030">`;
        chs[6].innerHTML = `<img src="/static/cards/28000011.png" class="cardimg" draggable="true" id="28000011">`;
        chs[7].innerHTML = `<img src="/static/cards/26000001.png" class="cardimg" draggable="true" id="26000001">`;
    } else if (deckname == "golemdragon") {
        chs[0].innerHTML = `<img src="/static/cards/26000009.png" class="cardimg" draggable="true" id="26000009">`;
        chs[1].innerHTML = `<img src="/static/cards/26000018.png" class="cardimg" draggable="true" id="26000018">`;
        chs[2].innerHTML = `<img src="/static/cards/26000015.png" class="cardimg" draggable="true" id="26000015">`;
        chs[3].innerHTML = `<img src="/static/cards/26000063.png" class="cardimg" draggable="true" id="26000063">`;
        chs[4].innerHTML = `<img src="/static/cards/28000012.png" class="cardimg" draggable="true" id="28000012">`;
        chs[5].innerHTML = `<img src="/static/cards/26000068.png" class="cardimg" draggable="true" id="26000068">`;
        chs[6].innerHTML = `<img src="/static/cards/28000015.png" class="cardimg" draggable="true" id="28000015">`;
        chs[7].innerHTML = `<img src="/static/cards/27000007.png" class="cardimg" draggable="true" id="27000007">`;
    }

    deck.update_deck((cardlist) => {
        hintlist.update(cardlist);
    });
}