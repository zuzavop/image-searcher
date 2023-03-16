/**
 *
 * @property {number} att
 * @property {number} lines
 * @property {number} displayed_classes
 * @property {boolean} showLastQuery
 * @property {boolean} similaritySearchEnabled
 * @property {string} photosAddress
 * @property {number} photosOnLine
 * @property {number} contextShift
 * @property {boolean} shiftInContextEnabled
 * @property {number[]} contextIds
 * @property {number} sizeDataset
 * @property {string} connection
 * @property {number} showingPhotos
 * @property {number} percGrow
 */
const config = {
    att: 2, // number of trying before next search image
    lines: 5,
    displayed_classes: 3,
    showLastQuery: true,
    similaritySearchEnabled: false,
    photosAddress: '../static/data/sea_photos/',
    photosOnLine: 12,
    contextShift: 3,
    shiftInContextEnabled: false,
    contextIds: [-2, -1, 0, 1, 2],
    sizeDataset: 22036, // 20000 for v3c and 22036 for sea dataset
    connection: ', ',
    showingPhotos: 60,
    percGrow: 1.4, // for sea dataset 1.4 and for v3c 9 - for scaling percentage of occurrence of classes
};

/**
 *
 * @property {string} cookies_warning
 * @property {string} similarity_warning
 * @property {string} context_warning
 * @property {string} right_answer
 * @property {string} warning
 * @property {string} last_warning
 * @property {string} wrong_answer
 */
const text_cz = {
    warning: "Povolte cookies, prosím! Následně načtěte znovu aktuální stránku.",
    last_warning: "Poslední dotaz před zobrazením dalšího hledané snímku.",
    similarity_warning: "Musí být vybrán nějaký snímek.",
    context_warning: "Kontext snímku nemůže být odeslán.",
    right_answer: "Správná odpověď. Nový hledaný snímek bude zobrazen.",
    wrong_answer: "Špatná odpověď. Zkuste to znovu.",
    cookies_warning: "Povolte cookies, prosím."
}

/**
 *
 * @property {string} cookies_warning
 * @property {string} similarity_warning
 * @property {string} context_warning
 * @property {string} right_answer
 * @property {string} warning
 * @property {string} last_warning
 * @property {string} wrong_answer
 */
const text_en = {
    warning: "Enable cookies, please! Then refresh this page.",
    last_warning: "Last search before displaying new search image.",
    similarity_warning: "Some image must be chosen.",
    context_warning: "Context of image can't be sent.",
    right_answer: "Right answer. New image will be generate.",
    wrong_answer: "Wrong answer. Try again.",
    cookies_warning: "Enable cookies, please."
}

const text = text_cz;