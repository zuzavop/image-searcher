const config = {
    att: 2, // number of trying before next search image
    lines: 5,
    showLastQuery: true,
    listingContext: false,
    photosAddress: '../static/data/sea_photos/',
    photosOnLine: 12,
    contextShift: 3,
    sizeDataset: 22036, // 20000 for v3c and 22036 for sea dataset
    connection: ', ',
    showingPhotos: 60,
    percGrow: 1.4, // for sea dataset 1.4 and for v3c 9 - for scaling percentage of occurrence of classes
};

const text_cz = {
    warning: "Povolte cookies, prosím! Následně načtěte znovu aktuální stránku.",
    last_warning: "Poslední dotaz před zobrazením dalšího hledané snímku.",
    similarity_warning: "Musí být vybrán nějaký snímek.",
    context_warning: "Kontext snímku nemůže být odeslán.",
    right_answer: "Správná odpověď. Nový hledaný snímek bude zobrazen.",
    wrong_answer: "Špatná odpověď. Zkuste to znovu.",
}

const text_en = {
    warning: "Enable cookies, please! Then refresh this page.",
    last_warning: "Last search before displaying new search image.",
    similarity_warning: "Some image must be chosen.",
    context_warning: "Context of image can't be sent.",
    right_answer: "Right answer. New image will be generate.",
    wrong_answer: "Wrong answer. Try again.",
}

const text = text_cz;