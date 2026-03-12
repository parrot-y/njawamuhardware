const CACHE_NAME = 'renovyte-v2';
/**
 * SERVICE WORKER KILL SWITCH
 * This file replaces the previous caching logic to destroy stale caches
 * and unregister the service worker from the browser.
 */

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    console.log('Destroying old cache:', cacheName);
                    return caches.delete(cacheName);
                })
            );
        }).then(() => {
            return self.registration.unregister();
        }).then(() => {
            console.log('Service Worker unregistered successfully.');
            return self.clients.matchAll();
        }).then((clients) => {
            clients.forEach(client => client.navigate(client.url));
        })
    );
});
