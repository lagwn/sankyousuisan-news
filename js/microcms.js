/**
 * microCMS API連携モジュール
 */
const MicroCMS = {
    /**
     * 記事一覧を取得
     * @param {number} limit - 取得件数
     * @returns {Promise<Object>} - 記事一覧データ
     */
    async getList(limit = 100) {
        const url = `https://${MICROCMS_CONFIG.serviceDomain}.microcms.io/api/v1/${MICROCMS_CONFIG.endpoint}?limit=${limit}&orders=-postDate`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-MICROCMS-API-KEY': MICROCMS_CONFIG.apiKey
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('記事一覧の取得に失敗しました:', error);
            throw error;
        }
    },

    /**
     * 記事詳細を取得
     * @param {string} id - 記事ID
     * @returns {Promise<Object>} - 記事詳細データ
     */
    async getDetail(id) {
        const url = `https://${MICROCMS_CONFIG.serviceDomain}.microcms.io/api/v1/${MICROCMS_CONFIG.endpoint}/${id}`;

        try {
            const response = await fetch(url, {
                headers: {
                    'X-MICROCMS-API-KEY': MICROCMS_CONFIG.apiKey
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('記事詳細の取得に失敗しました:', error);
            throw error;
        }
    },

    /**
     * 日付をフォーマット
     * @param {string} dateString - ISO形式の日付文字列
     * @returns {string} - YYYY/MM/DD形式
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}/${month}/${day}`;
    }
};
