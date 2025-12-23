/**
 * 詳細ページ用JavaScript
 */
document.addEventListener('DOMContentLoaded', async () => {
    const titleElement = document.getElementById('news-title');
    const bodyElement = document.getElementById('news-body');
    const dateElement = document.getElementById('news-date');

    // URLからIDを取得
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    if (!id) {
        titleElement.textContent = 'エラー';
        bodyElement.innerHTML = '<p>記事IDが指定されていません。</p>';
        return;
    }

    try {
        // 記事詳細を取得
        const data = await MicroCMS.getDetail(id);

        // ページタイトルを更新
        document.title = `三共水産株式会社-市場からの便り- » ${data.title}`;

        // コンテンツを表示（richContentを優先、なければrawContent）
        // richContent: リッチエディタ（新規投稿用）
        // rawContent: テキストエリア（既存投稿用）
        titleElement.textContent = data.title;
        const content = data.richContent || data.rawContent || '';
        const isRichContent = !!data.richContent;
        bodyElement.innerHTML = content;
        dateElement.textContent = `update: ${MicroCMS.formatDate(data.postDate || data.publishedAt)}`;

        // コンテンツ要素にIDを設定
        document.getElementById('news-content').id = `post-${data.id}`;

        // 画像レイアウトを処理
        processImageLayout(isRichContent);

    } catch (error) {
        titleElement.textContent = 'エラー';
        bodyElement.innerHTML = '<p>記事の読み込みに失敗しました。</p>';
        console.error(error);
    }
});

/**
 * 画像レイアウトを処理する
 * isRichContent=true: リッチエディタからのHTML（構造化済み）→連続画像のグリッド化のみ
 * isRichContent=false: rawContent（テキストエリア）→pタグなしでテキストノードとaタグが直接混在
 */
function processImageLayout(isRichContent = false) {
    const newsBody = document.getElementById('news-body');
    if (!newsBody) return;

    if (isRichContent) {
        // リッチエディタの場合：構造はそのまま、連続画像のみグリッド化
        processRichEditorContent(newsBody);
    } else {
        // テキストエリアの場合：従来の処理
        processRawContent(newsBody);
    }
}

/**
 * リッチエディタからのコンテンツを処理
 * 連続するfigure/img要素をグリッドにまとめる
 */
function processRichEditorContent(newsBody) {
    const nodes = Array.from(newsBody.childNodes);
    const fragment = document.createDocumentFragment();
    let imageGroup = [];

    const flushImageGroup = () => {
        if (imageGroup.length > 0) {
            const div = document.createElement('div');
            div.className = 'image-grid';
            imageGroup.forEach(item => {
                // figureからimgを取り出してaタグで包む
                const img = item.querySelector ? item.querySelector('img') : item;
                if (img) {
                    const a = document.createElement('a');
                    a.href = img.src;
                    a.setAttribute('data-lightbox', 'gallery');
                    const imgClone = img.cloneNode(true);
                    a.appendChild(imgClone);
                    div.appendChild(a);
                }
            });
            fragment.appendChild(div);
            imageGroup = [];
        }
    };

    nodes.forEach(node => {
        if (node.nodeType === Node.ELEMENT_NODE) {
            // figure要素（画像）の場合
            if (node.tagName === 'FIGURE' || (node.tagName === 'P' && node.querySelector('img'))) {
                imageGroup.push(node);
            }
            // div内に複数のfigureがある場合
            else if (node.tagName === 'DIV' && node.querySelector('figure')) {
                flushImageGroup();
                const figures = node.querySelectorAll('figure');
                if (figures.length > 0) {
                    const div = document.createElement('div');
                    div.className = 'image-grid';
                    figures.forEach(fig => {
                        const img = fig.querySelector('img');
                        if (img) {
                            const a = document.createElement('a');
                            a.href = img.src;
                            a.setAttribute('data-lightbox', 'gallery');
                            a.appendChild(img.cloneNode(true));
                            div.appendChild(a);
                        }
                    });
                    fragment.appendChild(div);
                }
            }
            else {
                flushImageGroup();
                fragment.appendChild(node.cloneNode(true));
            }
        } else if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
            flushImageGroup();
            fragment.appendChild(node.cloneNode(true));
        }
    });

    flushImageGroup();
    newsBody.innerHTML = '';
    newsBody.appendChild(fragment);
}

/**
 * テキストエリア（rawContent）からのコンテンツを処理
 * pタグなしでテキストノードとaタグが直接混在しているため構造化
 */
function processRawContent(newsBody) {

    // childNodesを配列に変換（ライブコレクションの問題を避ける）
    const nodes = Array.from(newsBody.childNodes);

    // 新しいコンテナを作成
    const fragment = document.createDocumentFragment();

    // 連続する画像リンクをグループ化するための一時配列
    let imageGroup = [];

    // 画像グループをフラッシュ（要素として追加）する関数
    const flushImageGroup = () => {
        if (imageGroup.length > 0) {
            const div = document.createElement('div');
            div.className = 'image-grid';
            imageGroup.forEach(img => div.appendChild(img.cloneNode(true)));
            fragment.appendChild(div);
            imageGroup = [];
        }
    };

    nodes.forEach(node => {
        // テキストノードの場合
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.textContent;
            if (text.trim().length > 0) {
                // 連続する画像があればまずフラッシュ
                flushImageGroup();

                // \n\nで分割して各セグメントを個別のpタグにする
                const segments = text.split(/\n\n+/);
                segments.forEach(segment => {
                    const trimmed = segment.trim();
                    if (trimmed.length === 0) return;

                    const p = document.createElement('p');
                    p.textContent = trimmed;

                    // 短いテキストで句点がなければセクションタイトルとする
                    if (trimmed.length < 50 && !trimmed.includes('。') && !trimmed.includes('、')) {
                        p.classList.add('section-title');
                    }
                    fragment.appendChild(p);
                });
            }
        }
        // 画像を含むaタグの場合
        else if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'A') {
            if (node.querySelector('img')) {
                // 画像リンクをグループに追加
                imageGroup.push(node);
            } else {
                // 画像なしのリンク
                flushImageGroup();
                fragment.appendChild(node.cloneNode(true));
            }
        }
        // h3などのブロック要素の場合
        else if (node.nodeType === Node.ELEMENT_NODE && ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'].includes(node.tagName)) {
            flushImageGroup();
            const clone = node.cloneNode(true);
            clone.classList.add('section-title');
            fragment.appendChild(clone);
        }
        // pタグの場合（既存のpタグがあれば）
        else if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'P') {
            flushImageGroup();
            const images = node.querySelectorAll('a:has(img), img');
            if (images.length > 0) {
                // 画像を含むpタグ
                const div = document.createElement('div');
                div.className = 'image-grid';
                images.forEach(img => {
                    if (img.tagName === 'A') {
                        div.appendChild(img.cloneNode(true));
                    } else if (img.parentElement.tagName !== 'A') {
                        div.appendChild(img.cloneNode(true));
                    }
                });
                fragment.appendChild(div);
            } else {
                // テキストのみのpタグ - <br>タグまたは改行で分割してセクションタイトルを抽出
                const html = node.innerHTML;
                const text = node.textContent;
                // <br>タグ（連続含む）で分割
                let parts = html.split(/(?:<br\s*\/?>\s*)+/i);

                // <br>タグで分割できなかった場合、textContentの改行文字で分割
                if (parts.length === 1) {
                    parts = text.split(/\n\n+/);
                }

                if (parts.length > 1) {
                    // 複数のパートがある場合、各パートを処理
                    parts.forEach((part, index) => {
                        // HTMLタグを除去してテキストのみ取得
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = part;
                        const trimmedPart = tempDiv.textContent.trim();
                        if (trimmedPart.length === 0) return;

                        const p = document.createElement('p');
                        p.textContent = trimmedPart;

                        // 最後のパートで、短くて句点で終わらないならセクションタイトル
                        if (index === parts.length - 1 &&
                            trimmedPart.length < 50 &&
                            !trimmedPart.endsWith('。') &&
                            !trimmedPart.endsWith('、')) {
                            p.classList.add('section-title');
                        }
                        fragment.appendChild(p);
                    });
                } else {
                    // 分割できない場合、テキスト内に潜在的なセクションタイトルがあるか確認
                    const text = node.textContent;
                    // 文の終わり（。）の後に短いテキストがある場合を検出
                    const match = text.match(/^(.+。)\s*([^。]{1,40})$/s);
                    if (match && match[2].trim().length > 2) {
                        const mainText = match[1].trim();
                        const titleText = match[2].trim();

                        // メインテキスト
                        const p1 = document.createElement('p');
                        p1.textContent = mainText;
                        fragment.appendChild(p1);

                        // セクションタイトル
                        const p2 = document.createElement('p');
                        p2.textContent = titleText;
                        p2.classList.add('section-title');
                        fragment.appendChild(p2);
                    } else {
                        // 通常のpタグとして追加
                        fragment.appendChild(node.cloneNode(true));
                    }
                }
            }
        }
        // その他の要素
        else if (node.nodeType === Node.ELEMENT_NODE) {
            flushImageGroup();
            fragment.appendChild(node.cloneNode(true));
        }
    });

    // 残っている画像グループをフラッシュ
    flushImageGroup();

    // 既存のコンテンツを置き換え
    newsBody.innerHTML = '';
    newsBody.appendChild(fragment);
}
