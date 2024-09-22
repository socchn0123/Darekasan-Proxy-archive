self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // リクエストURLを変更する例
    if (url.hostname === 'www.example.com') {
        url.hostname = 'proxy.example.com';
    }

    // 新しいリクエストを作成
    const modifiedRequest = new Request(url, {
        method: event.request.method,
        headers: event.request.headers,
        body: event.request.body,
        mode: event.request.mode,
        credentials: event.request.credentials,
        cache: event.request.cache,
        redirect: event.request.redirect,
        referrer: event.request.referrer,
        integrity: event.request.integrity
    });

    event.respondWith(
        fetch(modifiedRequest).then(response => {
            // レスポンスの内容を変更する例
            const modifiedResponse = new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: response.headers
            });

            return modifiedResponse;
        })
    );
});
