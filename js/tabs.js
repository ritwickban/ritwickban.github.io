// Function to open tabs
function openTab(tabName) {
    var i, tabContent;

    // Hide all tab content
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }

    // Show the selected tab content
    var selectedTab = document.getElementById(tabName);
    selectedTab.style.display = "block";

    // If the selected tab is "About Me," ensure it is visible regardless of scroll position
    if (tabName === "about") {
        selectedTab.style.opacity = 1;
    }
}
