// this JS is loaded on the deck page and is used to show the card image when
// hovering over a card in the deck list

// elements on the page have a 'sfid' attribute on the 'tr' element

// add event listeners to all tr elements of the table with id 'deck-table'
document.querySelectorAll('#deck-table tr, #deck-history tr').forEach(item => {
    item.addEventListener('mouseover', event => {
        // get the card id
        let card_id = item.getAttribute('sfid');

        if (card_id === null) {
            return;
        }

        // create the image element
        let img = document.createElement('img');
        img.src = `https://cards.scryfall.io/normal/front/${card_id.charAt(0)}/${card_id.charAt(1)}/${card_id}.jpg`;
        img.style.position = 'absolute';
        img.style.zIndex = 1;
        img.style.display = 'block';
        img.style.width = '200px';
        img.style.height = 'auto';
        img.style.top = `${event.clientY}px`;
        img.style.left = `${event.clientX}px`;
        img.id = 'card-image';
        img.style.border = '1px solid black';
        img.style.backgroundColor = 'white';
        img.style.padding = '5px';
        img.style.borderRadius = '5px';
        img.style.boxShadow = '5px 5px 5px black';

        // add the image to the body
        document.body.appendChild(img);

        // add event listener to the page so the image follows the mouse
        document.addEventListener('mousemove', event => {
            img.style.top = `${event.clientY}px`;
            img.style.left = `${event.clientX}px`;
        });
    });
    item.addEventListener('mouseout', event => {
        // remove the image
        let img = document.getElementById('card-image');

        if (img == null) {
          return;
        }

        img.parentNode.removeChild(img);
    });
})
