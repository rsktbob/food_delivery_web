// Initialize state
let restaurants = [];
let filteredRestaurants = [];
let filters = {
    cuisine: '',
    rating: 0,
    priceRange: '',
    sortBy: 'recommended',
    deliveryTime: ''
};
let searchTerm = '';

// Sample data (would come from API in real application)
const sampleRestaurants = [
    {
        id: 1,
        name: "Burger Palace",
        image: "https://via.placeholder.com/400x250",
        cuisine: "American",
        rating: 4.7,
        reviews: 243,
        deliveryTime: "20-30",
        priceRange: "$$",
        tags: ["Burgers", "Fast Food", "Fries"]
    },
    {
        id: 2,
        name: "Pizza Heaven",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Italian",
        rating: 4.5,
        reviews: 189,
        deliveryTime: "25-40",
        priceRange: "$$",
        tags: ["Pizza", "Pasta", "Italian"]
    },
    {
        id: 3,
        name: "Sushi King",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Japanese",
        rating: 4.8,
        reviews: 312,
        deliveryTime: "30-45",
        priceRange: "$$$",
        tags: ["Sushi", "Japanese", "Healthy"]
    },
    {
        id: 4,
        name: "Taco Express",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Mexican",
        rating: 4.4,
        reviews: 156,
        deliveryTime: "15-25",
        priceRange: "$",
        tags: ["Mexican", "Tacos", "Quick"]
    },
    {
        id: 5,
        name: "Curry House",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Indian",
        rating: 4.6,
        reviews: 205,
        deliveryTime: "35-50",
        priceRange: "$$",
        tags: ["Indian", "Curry", "Spicy"]
    },
    {
        id: 6,
        name: "Mediterranean Delight",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Mediterranean",
        rating: 4.5,
        reviews: 178,
        deliveryTime: "30-45",
        priceRange: "$$$",
        tags: ["Mediterranean", "Healthy", "Kebabs"]
    },
    {
        id: 7,
        name: "Wok & Roll",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Chinese",
        rating: 4.3,
        reviews: 167,
        deliveryTime: "25-35",
        priceRange: "$$",
        tags: ["Chinese", "Noodles", "Stir Fry"]
    },
    {
        id: 8,
        name: "Green Garden",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Vegetarian",
        rating: 4.6,
        reviews: 198,
        deliveryTime: "25-40",
        priceRange: "$$",
        tags: ["Vegetarian", "Vegan", "Healthy"]
    },
    {
        id: 9,
        name: "Breakfast Club",
        image: "https://via.placeholder.com/400x250",
        cuisine: "American",
        rating: 4.5,
        reviews: 134,
        deliveryTime: "20-30",
        priceRange: "$$",
        tags: ["Breakfast", "Brunch", "Coffee"]
    },
    {
        id: 10,
        name: "Thai Spice",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Thai",
        rating: 4.7,
        reviews: 221,
        deliveryTime: "30-45",
        priceRange: "$$",
        tags: ["Thai", "Spicy", "Noodles"]
    },
    {
        id: 11,
        name: "Steakhouse Prime",
        image: "https://via.placeholder.com/400x250",
        cuisine: "American",
        rating: 4.9,
        reviews: 267,
        deliveryTime: "40-55",
        priceRange: "$$$$",
        tags: ["Steak", "Grill", "Fine Dining"]
    },
    {
        id: 12,
        name: "Pho Corner",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Vietnamese",
        rating: 4.6,
        reviews: 183,
        deliveryTime: "25-40",
        priceRange: "$$",
        tags: ["Vietnamese", "Soup", "Noodles"]
    },
    {
        id: 13,
        name: "Falafel House",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Mediterranean",
        rating: 4.4,
        reviews: 142,
        deliveryTime: "20-35",
        priceRange: "$",
        tags: ["Falafel", "Hummus", "Vegetarian"]
    },
    {
        id: 14,
        name: "Seafood Harbor",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Seafood",
        rating: 4.8,
        reviews: 231,
        deliveryTime: "35-50",
        priceRange: "$$$",
        tags: ["Seafood", "Fish", "Grill"]
    },
    {
        id: 15,
        name: "Pasta Palace",
        image: "https://via.placeholder.com/400x250",
        cuisine: "Italian",
        rating: 4.7,
        reviews: 197,
        deliveryTime: "30-45",
        priceRange: "$$$",
        tags: ["Pasta", "Italian", "Wine"]
    }
];

// Helper function to render stars
function renderStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    let starsHTML = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
        starsHTML += '<i class="fas fa-star"></i>';
    }
    
    // Half star
    if (halfStar) {
        starsHTML += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        starsHTML += '<i class="far fa-star"></i>';
    }
    
    return starsHTML;
}

// Function to render restaurant cards
function renderRestaurants() {
    const restaurantCardsContainer = document.getElementById('restaurant-cards');
    const noResultsElement = document.getElementById('no-results');
    const resultsCountElement = document.getElementById('results-count');
    
    // Update results count
    resultsCountElement.textContent = `Showing ${filteredRestaurants.length} restaurants`;
    
    // Show/hide no results message
    if (filteredRestaurants.length === 0) {
        noResultsElement.style.display = 'block';
        restaurantCardsContainer.style.display = 'none';
    } else {
        noResultsElement.style.display = 'none';
        restaurantCardsContainer.style.display = 'grid';
        
        // Generate HTML for restaurant cards
        restaurantCardsContainer.innerHTML = '';
        
        filteredRestaurants.forEach(restaurant => {
            const card = document.createElement('div');
            card.className = 'restaurant-card';
            card.dataset.id = restaurant.id;
            
            // Generate tags HTML
            const tagsHTML = restaurant.tags.map(tag => 
                `<span class="tag">${tag}</span>`
            ).join('');
            
            card.innerHTML = `
                <div class="restaurant-image">
                    <img src="${restaurant.image}" alt="${restaurant.name}" />
                    <span class="delivery-time">${restaurant.deliveryTime} min</span>
                </div>
                <div class="restaurant-info">
                    <div class="restaurant-name-price">
                        <h3>${restaurant.name}</h3>
                        <span class="price-range">${restaurant.priceRange}</span>
                    </div>
                    <p class="restaurant-cuisine">${restaurant.cuisine}</p>
                    <div class="restaurant-rating">
                        <div class="stars">
                            ${renderStars(restaurant.rating)}
                        </div>
                        <span class="rating-text">
                            ${restaurant.rating} (${restaurant.reviews})
                        </span>
                    </div>
                    <div class="restaurant-tags">
                        ${tagsHTML}
                    </div>
                </div>
            `;
            
            // Add click event listener
            card.addEventListener('click', () => {
                handleRestaurantClick(restaurant.id);
            });
            
            restaurantCardsContainer.appendChild(card);
        });
    }
}

// Function to filter restaurants
function filterRestaurants() {
    let results = restaurants;
    
    // Apply search filter
    if (searchTerm) {
        results = results.filter(restaurant => 
            restaurant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            restaurant.cuisine.toLowerCase().includes(searchTerm.toLowerCase()) ||
            restaurant.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
        );
    }
    
    // Apply cuisine filter
    if (filters.cuisine) {
        results = results.filter(restaurant => 
            restaurant.cuisine === filters.cuisine
        );
    }
    
    // Apply rating filter
    if (filters.rating > 0) {
        results = results.filter(restaurant => 
            restaurant.rating >= filters.rating
        );
    }
    
    // Apply price range filter
    if (filters.priceRange) {
        results = results.filter(restaurant => 
            restaurant.priceRange === filters.priceRange
        );
    }
    
    // Apply delivery time filter
    if (filters.deliveryTime) {
        results = results.filter(restaurant => {
            const maxTime = parseInt(restaurant.deliveryTime.split('-')[1]);
            if (filters.deliveryTime === 'under30' && maxTime <= 30) return true;
            if (filters.deliveryTime === '30to45' && maxTime > 30 && maxTime <= 45) return true;
            if (filters.deliveryTime === 'over45' && maxTime > 45) return true;
            return false;
        });
    }
    
    // Apply sorting
    if (filters.sortBy === 'rating') {
        results = [...results].sort((a, b) => b.rating - a.rating);
    } else if (filters.sortBy === 'deliveryTime') {
        results = [...results].sort((a, b) => {
            const aTime = parseInt(a.deliveryTime.split('-')[0]);
            const bTime = parseInt(b.deliveryTime.split('-')[0]);
            return aTime - bTime;
        });
    } else if (filters.sortBy === 'priceAsc') {
        results = [...results].sort((a, b) => {
            const priceOrder = { '$': 1, '$$': 2, '$$$': 3, '$$$$': 4 };
            return priceOrder[a.priceRange] - priceOrder[b.priceRange];
        });
    } else if (filters.sortBy === 'priceDesc') {
        results = [...results].sort((a, b) => {
            const priceOrder = { '$': 1, '$$': 2, '$$$': 3, '$$$$': 4 };
            return priceOrder[b.priceRange] - priceOrder[a.priceRange];
        });
    }
    
    filteredRestaurants = results;
    renderRestaurants();
}

// Function to handle restaurant click
function handleRestaurantClick(id) {
    // In the original React app, this would navigate to a restaurant detail page
    // For this vanilla JS version, we'll just alert for demo purposes
    alert(`Navigating to restaurant with ID: ${id}`);
    // In a real application, you might do: window.location.href = `/restaurant/${id}`;
}

// Function to reset filters
function resetFilters() {
    // Reset filters object
    filters = {
        cuisine: '',
        rating: 0,
        priceRange: '',
        sortBy: 'recommended',
        deliveryTime: ''
    };
    searchTerm = '';
    
    // Reset UI elements
    document.getElementById('search-input').value = '';
    document.getElementById('cuisine-filter').value = '';
    document.getElementById('delivery-filter').value = '';
    document.getElementById('sort-filter').value = 'recommended';
    
    // Reset rating options
    document.querySelectorAll('.rating-option').forEach(option => {
        option.classList.remove('active');
        if (option.dataset.rating === '0') {
            option.classList.add('active');
        }
    });
    
    // Reset price options
    document.querySelectorAll('.price-option').forEach(option => {
        option.classList.remove('active');
        if (option.dataset.price === '') {
            option.classList.add('active');
        }
    });
    
    // Update filtered restaurants
    filterRestaurants();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize data
    restaurants = sampleRestaurants;
    filteredRestaurants = sampleRestaurants;
    
    // Render initial restaurants
    renderRestaurants();
    
    // Search input
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value;
        filterRestaurants();
    });
    
    // Cuisine filter
    const cuisineFilter = document.getElementById('cuisine-filter');
    cuisineFilter.addEventListener('change', (e) => {
        filters.cuisine = e.target.value;
        filterRestaurants();
    });
    
    // Rating options
    document.querySelectorAll('.rating-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.rating-option').forEach(opt => {
                opt.classList.remove('active');
            });
            option.classList.add('active');
            filters.rating = parseFloat(option.dataset.rating);
            filterRestaurants();
        });
    });
    
    // Price options
    document.querySelectorAll('.price-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.price-option').forEach(opt => {
                opt.classList.remove('active');
            });
            option.classList.add('active');
            filters.priceRange = option.dataset.price;
            filterRestaurants();
        });
    });
    
    // Delivery time filter
    const deliveryFilter = document.getElementById('delivery-filter');
    deliveryFilter.addEventListener('change', (e) => {
        filters.deliveryTime = e.target.value;
        filterRestaurants();
    });
    
    // Sort filter
    const sortFilter = document.getElementById('sort-filter');
    sortFilter.addEventListener('change', (e) => {
        filters.sortBy = e.target.value;
        filterRestaurants();
    });
    
    // Reset filters buttons
    document.getElementById('reset-filters-btn').addEventListener('click', resetFilters);
    document.getElementById('reset-search-btn').addEventListener('click', resetFilters);
});