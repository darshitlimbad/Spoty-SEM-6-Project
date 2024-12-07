document.getElementById('discord-login').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    if (username.trim()) {
      alert(`Hello, ${username}! Redirecting to Discord login...`);
    } else {
      alert('Please enter a username.');
    }
});
  
