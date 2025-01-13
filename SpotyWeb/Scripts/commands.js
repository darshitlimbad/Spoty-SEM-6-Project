document.addEventListener('DOMContentLoaded', function () {
    fetchCategorizedCommands();
});

async function fetchCategorizedCommands() {
    try {
        const commandsResponse = await fetch('../json/commands.json');
        const commandsData = await commandsResponse.json();

        const tableBody = document.getElementById('all-commands-table-body');
        if (tableBody) {
            commandsData.commandCategories.forEach(category => {
                const categoryRow = tableBody.insertRow();
                const categoryCell = categoryRow.insertCell();
                categoryCell.colSpan = 3; // Span across all columns
                 categoryCell.textContent = category.name;
                  categoryCell.style.fontWeight = 'bold'; // Make category name bold
                categoryCell.style.textAlign= 'center';

                category.commands.forEach(command => {
                    const row = tableBody.insertRow();
                    const nameCell = row.insertCell();
                    nameCell.textContent = command.name;
                    
                    const descriptionCell = row.insertCell();
                    descriptionCell.textContent = command.description;

                    const planCell = row.insertCell();
                    planCell.innerHTML = command.premium ? '<span style="color:#f44336;">Premium</span>' : '<span style="color:#4caf50;">Free</span>';
                });
            });
        }

    } catch (error) {
        console.error('Error fetching categorized commands:', error);
    }
}