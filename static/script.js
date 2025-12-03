console.log("hello world!");

function clear_deck() {
    deck.clear();
    hintlist.update([]);
}

function deck_update_callback(cardlist) {
    hintlist.update(cardlist);
}

function dragstartHandler(ev) { ev.dataTransfer.setData("text", ev.target.id); }
function dragoverHandler(ev) {
    ev.preventDefault();
}
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

    deck.update_deck(deck_update_callback);
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
    constructor() {
        this.cards = [];
        this.avgcost = 0;
    }

    async update_deck(callback) {
        const holders = document.getElementsByClassName("cardholder");
        this.cards = [];

        for (let cardholder of holders) {
            if (cardholder.childElementCount > 0) {
                let cardjson = await getJSON(`/cardid/${cardholder.children[0].id}`);
                this.cards.push(cardjson);
            }
        }

        this.update_elixir();
        callback(this.cards);
    }

    update_elixir() {
        let totalelixir = 0;
        for (let card of this.cards) {
            totalelixir += card.cost;
        }
        this.avgcost = totalelixir / this.cards.length;
        if (this.cards.length == 0) this.avgcost = 0;
        document.getElementById("avgelixir").innerHTML = this.avgcost.toFixed(1);
    }

    clear() {
        const holders = document.getElementsByClassName("cardholder");
        this.cards = [];
        for (let cardholder of holders) {
            cardholder.innerHTML = "";
        }
        this.update_elixir();
    }
}

// lower left holder for suggestions to the current deck
class HintList {
    constructor() {
        this.hh = document.getElementById("hintholder");
    }

    add_warning(message) {
        let warning = document.createElement("span");
        warning.innerHTML = message;
        warning.classList.add("warning");
        this.hh.appendChild(warning);
    }

    add_mistake(message) {
        let mistake = document.createElement("span");
        mistake.innerHTML = message;
        mistake.classList.add("mistake");
        this.hh.appendChild(mistake);
    }

    update(cardlist) {
        console.log("running hint update on cardlist: ");
        console.log(cardlist);
        this.hh.innerHTML = "";

        // **Mistakes**
        // Empty deck
        if (cardlist.length == 0) {
            this.add_mistake("Empty deck");
            return;
        }

        // Does not contain a WinConditions
        if (tagcount(cardlist, "WinCondition") == 0) {
            this.add_mistake("Must contain a Win Condition");
        }

        // Does not contain an Air Defense
        if (tagcount(cardlist, "AirDefense") == 0) {
            this.add_mistake("Must contain Air Defense");
        }

        // Contains a duplicate card
        let idset = new Set();
        for (let card of cardlist) {
            idset.add(card.card_id);
        }
        if (idset.length < cardlist.length) {
            this.add_mistake("Contains a duplicate card");
        }

        // **Warnings**
        // Average elixir cost too high (> 8)
        let totalelixir = 0;
        for (let card of cardlist) {
            totalelixir += card.cost;
        }
        if ((totalelixir / cardlist.length) >= 8) {
            this.add_warning("Average elixir cost too high (>= 8)");
        }

        // Does not contain a WinCondition
        if (tagcount(cardlist, "WinCondition") == 1) {
            this.add_warning("Should contain 2 WinConditions");
        }

        // Does not contain a Building
        if(tagcount(cardlist, "Building") == 0) {
            this.add_warning("Should contain a Building");
        }

        // Does not contain a MiniTank
        if(tagcount(cardlist, "MiniTank") == 0) {
            this.add_warning("Should contain a MiniTank");
        }

        // Does not contain an AoE or Spell card
        if(tagcount(cardlist, "AoE") == 0 && tagcount(cardlist, "Spell") == 0) {
            this.add_warning("No Swarm defense");
        }
    }
}