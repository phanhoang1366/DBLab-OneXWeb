document.addEventListener('DOMContentLoaded', function() {
    const novelField = document.getElementById('id_novel');
    const chapterNumberField = document.getElementById('id_chapter_number');
    if (novelField) {
        novelField.addEventListener('change', function() {
            const novelId = this.value;
            if (novelId) {
                fetch(`/admin/onexweb/chapter/next_chapter_number/?novel_id=${novelId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (chapterNumberField) {
                            chapterNumberField.value = data.next_chapter_number;
                        }
                    });
            }
        });
    }
});