document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const resultsCount = document.querySelector('.results-count');
    const noResults = document.querySelector('.no-results');
    const categories = document.querySelectorAll('.category');

    // 搜索功能
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase().trim();

        if (searchTerm === '') {
            // 如果搜索框为空，重置所有显示状态
            categories.forEach(category => {
                category.classList.remove('hidden');
                const links = category.querySelectorAll('.link-card');
                links.forEach(link => {
                    link.style.display = 'flex';  // 重置所有链接为显示状态
                });
            });
            searchResults.style.display = 'none';
            return;
        }

        // 遍历所有分类和链接
        let matchCount = 0;
        categories.forEach(category => {
            const categoryName = category.querySelector('h2').textContent.toLowerCase();
            const links = category.querySelectorAll('.link-card');
            let categoryHasMatch = false;

            links.forEach(link => {
                const title = link.querySelector('h3').textContent.toLowerCase();
                const description = link.querySelector('p').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || 
                    description.includes(searchTerm) || 
                    categoryName.includes(searchTerm)) {
                    link.style.display = 'flex';
                    categoryHasMatch = true;
                    matchCount++;
                } else {
                    link.style.display = 'none';
                }
            });

            // 如果分类中有匹配项，显示该分类，否则隐藏
            if (categoryHasMatch) {
                category.classList.remove('hidden');
            } else {
                category.classList.add('hidden');
            }
        });

        // 更新搜索结果显示
        searchResults.style.display = 'block';
        if (matchCount > 0) {
            resultsCount.textContent = `找到 ${matchCount} 个相关结果`;
            noResults.style.display = 'none';
        } else {
            resultsCount.textContent = '';
            noResults.style.display = 'block';
        }
    });

    // 添加一个重置按钮（可选）
    const searchBox = document.querySelector('.search-box');
    const resetButton = document.createElement('button');
    resetButton.type = 'button';
    resetButton.className = 'reset-search';
    resetButton.innerHTML = '✕';
    resetButton.style.cssText = `
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: #999;
        cursor: pointer;
        font-size: 16px;
        padding: 5px;
        display: none;
    `;
    
    // 让 search-box 成为相对定位的容器
    searchBox.style.position = 'relative';
    searchBox.appendChild(resetButton);

    // 显示/隐藏重置按钮
    searchInput.addEventListener('input', function() {
        resetButton.style.display = this.value ? 'block' : 'none';
    });

    // 点击重置按钮清空搜索
    resetButton.addEventListener('click', function() {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        this.style.display = 'none';
    });

    // 链接点击统计
    document.querySelectorAll('.link-card').forEach(link => {
        link.addEventListener('click', function() {
            const linkData = {
                title: this.querySelector('h3').textContent,
                url: this.href,
                timestamp: new Date().toISOString()
            };
            
            // 这里可以添加访问统计的代码
            console.log('Link clicked:', linkData);
        });
    });
}); 