all_articles = $("div.article-summary");
selected_category = "all";

function highlight_category(category) {
    $("li.".concat(selected_category)).removeClass("active");
    $("li.".concat(category)).addClass("active");
    selected_category = category;
    var filtered_articles = all_articles.filter(".".concat(category));
    if (category == "all") {
        filtered_articles = all_articles;
    }
    $("div#article-listing-container").html(filtered_articles);
}
