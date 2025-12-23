/**
 * 一覧ページ用JavaScript
 */
document.addEventListener('DOMContentLoaded', async () => {
    const listElement = document.getElementById('news-list');

    try {
        // 記事一覧を取得
        const data = await MicroCMS.getList(100);

        // リストをクリア
        listElement.innerHTML = '';

        if (data.contents.length === 0) {
            listElement.innerHTML = '<li>記事がありません</li>';
            return;
        }

        // 記事をリストに追加
        data.contents.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
        <span class="date">${MicroCMS.formatDate(item.postDate || item.publishedAt)}</span>
        <a href="detail.html?id=${item.id}" id="post-${item.id}">${escapeHtml(item.title)}</a>
      `;
            listElement.appendChild(li);
        });

    } catch (error) {
        listElement.innerHTML = `<li class="error">記事の読み込みに失敗しました。<br>設定を確認してください。</li>`;
        console.error(error);
    }
});

/**
 * HTMLエスケープ
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
