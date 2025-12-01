console.log("hello world!")

function dragstartHandler(ev) { ev.dataTransfer.setData("text", ev.target.id); }
function dragoverHandler(ev) { ev.preventDefault(); }
function dropHandler(ev) {
    console.log(ev);
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text");

    let newelement = document.getElementById(data);
    let oldelement;
    if (ev.target.nodeName == "IMG") {
        oldelement = ev.target.parentNode;
    } else {
        oldelement = ev.target;
    }

    console.log(`dragging into ${oldelement.id}`);
    if (oldelement.id == "pickercards") {
        // dragging into the picker area
        oldelement.appendChild(newelement);
    } else if (oldelement.id.slice(0, 4) == "deck") {
        // dragging into a deck slot
        let replacecard = (oldelement.childElementCount > 0);
        let old;
        if (replacecard) old = oldelement.children[0].cloneNode(false);
        oldelement.innerHTML = "";
        oldelement.appendChild(newelement);
        if (replacecard) document.getElementById("pickercards").appendChild(old);
    } else {
        // invalid
        console.log("invalid drag");
    }
}

// right pane w/ filter buttons and draggable card images
class Picker {
    constructor() {
        this.filter_tag = "";
    }

    deselect_filterbtns() {
        for (let fbtn of document.getElementsByClassName("filterbtn")) {
            fbtn.children[0].src = "/static/button/redleft.png";
            fbtn.children[1].style["backgroundImage"] = "url('/static/button/redmid.png')";
            fbtn.children[2].src = "/static/button/redright.png";
        }
    }

    filter_by(filterbtn, tag) {
        console.log(`filtering by ${tag}`);
        this.filter_tag = tag;
        this.deselect_filterbtns();

        filterbtn.children[0].src = "/static/button/greenleft.png";
        filterbtn.children[1].style["backgroundImage"] = "url('/static/button/greenmid.png')";
        filterbtn.children[2].src = "/static/button/greenright.png";

        this.populate_picker(tag);
    }

    async populate_picker(tag) {
        let cardjson = await getJSON(`/cards/${tag}`);
        document.getElementById("pickercards").innerHTML = "";

        for (var card of cardjson) {
            let cardimg = document.createElement("img");
            cardimg.src = `/static/cards/${card.card_id}.png`;
            cardimg.classList.add("cardimg");
            cardimg.draggable = true;
            cardimg.id = card.card_id;
            cardimg.ondragstart = function() {
                dragstartHandler(event);
            }
            document.getElementById("pickercards").append(cardimg);
        }
    }
}

// upper left holder for selected cards
class Deck {

}

// lower left holder for suggestions to the current deck
class HintList {

}