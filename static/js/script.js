const rangeLabel = document.querySelector('.custom-range-slider');
const rangeInput = rangeLabel.children[0];
const thumbWidth = 200;

rangeLabel.insertAdjacentHTML(
    'beforeend',
    `<span class="bubble"></span>`
);

const rangeBubble = rangeLabel.children[1];

positionBubble(rangeBubble, rangeInput)

function positionBubble(bubbleElement, anchorElement) {
    const { min, max, value, offsetWidth } = anchorElement;
    const total = Number(max) - Number(min);
    const perc = (Number(value) - Number(min)) / total;
    const offset = (thumbWidth / 2) - (thumbWidth * perc);

    bubbleElement.textContent = 'R$ '+value;
}

rangeInput.addEventListener('input', (e) => positionBubble(rangeBubble, e.target))


let checkbox = document.getElementById("fruit1");
let date_volta = document.getElementById('date-volta')


checkbox.addEventListener('change', function (e) {
    let volta_required = document.getElementById('required-volta')
    if (checkbox.checked) {
        date_volta.disabled = true
        volta_required.style.color = 'transparent'
    }
    else {
        date_volta.disabled = false
        volta_required.style.color = "red"
    }
});

let names = [
    "SSA",
    "GRU",
    "BSB",
    "CGH",
    "GIG",
    "FLN",
    "POA",
    "VCP",
    "REC",
    "CWB",
    "BEL",
    "VIX",
    "SDU",
    "CGB",
    "CGR",
    "FOR",
    "MCP",
    "MGF",
    "GYN",
    "NVT",
    "MAO",
    "NAT",
    "BPS",
    "MCZ",
    "PMW",
    "SLZ",
    "LDB",
    "PVH",
    "RBR",
    "JOI",
    "UDI",
    "CXJ",
    "IGU",
    "THE",
    "AJU",
    "JPA",
    "PNZ",
    "CNF",
    "BVB",
    "CPV",
    "STM",
    "IOS",
    "JDO",
    "IMP",
    "XAP",
    "MAB",
    "CZS",
    "PPB",
    "CFB",
    "FEN",
    "JTC",
    "MOC",
];

let sortedNames = names.sort();

let input = document.getElementById("input");
let input1 = document.getElementById("input1");
let btn_r = document.getElementById("btn-r")

input.addEventListener("keyup", (e) => {
    removeElements();
    for (let i of sortedNames) {
        if (
            i.toLowerCase().startsWith(input.value.toLowerCase()) &&
            input.value != ""
        ) {
            let listItem = document.createElement("li");
            listItem.classList.add("list-items");
            listItem.style.cursor = "pointer";
            listItem.setAttribute("onclick", "displayNames('" + i + "')");
            let word = "<b>" + i.substr(0, input.value.length) + "</b>";
            word += i.substr(input.value.length);
            listItem.innerHTML = word;
            document.querySelector(".list").appendChild(listItem);
        }
    }
});
input1.addEventListener("keyup", (e) => {
    removeElementstwo();
    for (let i of sortedNames) {

        if (
            i.toLowerCase().startsWith(input1.value.toLowerCase()) &&
            input1.value != ""
        ) {
            let listItem = document.createElement("li");
            listItem.classList.add("list-items-two");
            listItem.style.cursor = "pointer";
            listItem.setAttribute("onclick", "displayNamestwo('" + i + "')");
            let word = "<b>" + i.substr(0, input1.value.length) + "</b>";
            word += i.substr(input1.value.length);
            listItem.innerHTML = word;
            document.querySelector(".list-two").appendChild(listItem);
        }
    }
});

function displayNames(value) {
    input.value = value;
    removeElements();
}
function displayNamestwo(value) {
    input1.value = value;
    removeElementstwo();
}
function removeElements() {
    let items = document.querySelectorAll(".list-items");
    items.forEach((item) => {
        item.remove();
    });
}
function removeElementstwo() {
    let items = document.querySelectorAll(".list-items-two");
    items.forEach((item) => {
        item.remove();
    });
}

btn_r.addEventListener("click", () => {
    let aux = input.value

    input.value = input1.value;
    input1.value = aux;

})