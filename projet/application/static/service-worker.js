self.addEventListener('install', (event) => {
    console.log('Service Worker installé');
});

self.addEventListener('fetch', (event) => {
    console.log('Interception requête :', event.request.url);
});
