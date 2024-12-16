// Sample Categories Array
let categories = [
    {
        name: 'Electronics',
        image: 'https://via.placeholder.com/150'
    },
    {
        name: 'Clothing',
        image: 'https://via.placeholder.com/150'
    }
];

// Load categories on the list page
document.addEventListener("DOMContentLoaded", function () {
    const categoryList = document.getElementById('categoryList');

    if (categoryList) {
        categories.forEach(category => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><img src="${category.image}" alt="${category.name}" /></td>
                <td>${category.name}</td>
                <td>
                    <button onclick="editCategory('${category.name}')">Edit</button>
                    <button onclick="deleteCategory('${category.name}')">Delete</button>
                </td>
            `;
            categoryList.appendChild(row);
        });
    }

    // Handle Add/Edit Category Page
    const urlParams = new URLSearchParams(window.location.search);
    const categoryName = urlParams.get('categoryName');
    if (categoryName) {
        const categoryToEdit = categories.find(cat => cat.name === categoryName);
        if (categoryToEdit) {
            document.getElementById('formTitle').textContent = 'Edit Category';
            document.getElementById('categoryName').value = categoryToEdit.name;
            document.getElementById('previewImage').src = categoryToEdit.image;
            document.getElementById('previewImage').style.display = 'block';
        }
    }

    // Image Preview
    const imageInput = document.getElementById('categoryImage');
    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            const reader = new FileReader();
            reader.onload = function () {
                const previewImage = document.getElementById('previewImage');
                previewImage.src = reader.result;
                previewImage.style.display = 'block';
            };
            reader.readAsDataURL(e.target.files[0]);
        });
    }

    // Handle form submit for adding/editing
    const categoryForm = document.getElementById('categoryForm');
    if (categoryForm) {
        categoryForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const name = document.getElementById('categoryName').value;
            const image = document.getElementById('previewImage').src;

            if (categoryName) {
                // Update existing category
                const categoryToEdit = categories.find(cat => cat.name === categoryName);
                categoryToEdit.name = name;
                categoryToEdit.image = image;
                alert(`Category ${categoryName} updated to ${name}.`);
            } else {
                // Add new category
                categories.push({ name, image });
                alert(`Category ${name} added.`);
            }
            window.location.href = 'category-list.html';
        });
    }
});

// Edit Category
function editCategory(categoryName) {
    window.location.href = `add-category.html?categoryName=${categoryName}`;
}

// Delete Category
function deleteCategory(categoryName) {
    if (confirm(`Are you sure you want to delete the category: ${categoryName}?`)) {
        categories = categories.filter(cat => cat.name !== categoryName);
        alert(`${categoryName} deleted.`);
        window.location.reload();
    }
}
