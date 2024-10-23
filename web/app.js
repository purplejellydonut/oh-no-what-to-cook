// let validGroceryItem = [];

function addGroceryItem(name, qty) {
    const groceryList = document.getElementById('grocery-list');
    // Check if the item is valid
    // const validItem = validGroceryItem.find(item => item === name);

    // if (!validItem) {
    //     // Show an error message if the item already exists
    //     alert(`${name} is not a valid option.`);
    //     return -1;
    // }
    // Check if the item already exists
    const existingItem = Array.from(groceryList.getElementsByClassName('grocery-item'))
        .find(item => item.querySelector('.item-name').textContent === name);

    if (existingItem) {
        // Show an error message if the item already exists
        alert(`${name} already exists in the grocery list.`);
        return -1;
    }
    // Create new grocery item if it does not exist
    const listItem = document.createElement('li');
    listItem.className = 'grocery-item';

    listItem.innerHTML = `
            <span class="item-name">${name}${qty ? "("+qty+")" : ""}</span>
        `;

    groceryList.appendChild(listItem);
}

document.addEventListener('DOMContentLoaded', function () {
    const recipeResults = document.getElementById('recipe-results');
    const addGroceryItemButton = document.getElementById('add-grocery-item');
    const findRecipesButton = document.getElementById('find-recipes');

    // fetch('http://127.0.0.1:8000/grocery-items', {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    // })
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error("API request failed with status: " + response.status);
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         data.forEach(item => {
    //             validGroceryItem.push(item.name);
    //             console.log(validGroceryItem)
    //         })
    //     })

    let groceryItems = [];

    addGroceryItemButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission
        const itemName = document.getElementById('item-name').value.trim().toLowerCase();
        const itemQty = document.getElementById('item-qty').value || null;

        if (itemName) {
            addGroceryItem(itemName, itemQty);
            groceryItems.push({
                name: itemName,
                qty: itemQty
            });
        } else {
            alert('Please enter a grocery item name.');
        }

        // Clear input fields after adding the item
        document.getElementById('item-name').value = '';
        document.getElementById('item-qty').value = '';
    });

    document.addEventListener('keydown', function (event) {
        if (event.shiftKey && event.key === 'Enter') {
            event.preventDefault();
            findRecipesButton.click();
        }
    })

    findRecipesButton.addEventListener('click', function () {
        console.log("Sending request with grocery items:", groceryItems);

        fetch('http://127.0.0.1:8000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(groceryItems),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("API request failed with status: " + response.status);
                }
                return response.json();
            })
            .then(data => {
                console.log("Received response:", data);  // Check the response structure

                // Clear previous results
                recipeResults.innerHTML = '';

                // Check if there are any recipes
                if (data.length === 0) {
                    recipeResults.innerHTML = '<p>No matching recipes found.</p>';
                    return;
                }

                // Iterate and display recipes
                data.forEach(recipe => {
                    const recipeDiv = document.createElement('div');
                    recipeDiv.className = 'recipe';

                    // Split instructions by full stops, trim each part, and enumerate them
                    const formattedInstructions = recipe.instruction
                        .split('.')
                        .map((sentence, index) => sentence.trim())  // Trim each sentence
                        .filter(sentence => sentence.length > 0)    // Remove empty sentences
                        .map((sentence, index) => `${index + 1}. ${sentence}`)  // Add step numbers
                        .join('.<br>');  // Join sentences with a period and a new line

                    recipeDiv.innerHTML = `<h3>${recipe.name}</h3>
                                       <p><strong>Ingredients:</strong> ${recipe.ingredients.map(item => item.name + "(" + item.qty + ")").join(', ')}</p>
                                       <p><strong>Instructions:</strong><br>${formattedInstructions}.</p>`;  // Add final period
                    recipeResults.appendChild(recipeDiv);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                recipeResults.innerHTML = '<p>Error fetching recipes.</p>';
            });
    });

});
