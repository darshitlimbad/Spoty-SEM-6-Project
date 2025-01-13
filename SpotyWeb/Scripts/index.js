document.addEventListener('DOMContentLoaded', function () {
    initDiscordLoginBtn();
    fetchData();
});
  

// Handle Discord login button clicks
function initDiscordLoginBtn(){
  document.querySelectorAll('#discord-login').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        // Replace with actual Discord OAuth URL
        window.location.href = 'https://discord.com/oauth2/authorize';
    });
  });
}

// Fetch data from the server
function fetchData(){

  //1. Fetch features data from JSON and populate the features section
  fetch('./json/features.json')
  .then(response => response.json())
  .then(data => {
      const featuresContainer = document.getElementById('features-container');
      data.features.forEach(feature => {
          const featureBox = document.createElement('div');
          featureBox.classList.add('feature-box');

          const title = document.createElement('h3');
          title.textContent = feature.title;
          
          const description = document.createElement('p');
          description.textContent = feature.description;

          featureBox.appendChild(title);
          featureBox.appendChild(description);
          featuresContainer.appendChild(featureBox);
      });
  })
  .catch(error => console.error('Error fetching features:', error));
}
