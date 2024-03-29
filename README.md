# Uralic Typological database (UraTyp)

The UraTyp dataset includes information on 360 features spanning the domains of morphology, syntax, phonology, and marginally also lexicon collected from all the branches of the Uralic language family. 195 out of 360 features were collected using the Grambank questionnaire (i.e. the GB list of features), which was developed by the Grambank team to collect data from about half of the world’s languages (https://glottobank.org/). GB list of features and the development of the data will be presented elsewhere (Skirgård et al., 2023). The remaining 165 features (i.e. the UT list of features) were developed by the author team of the UraTyp database to further explore the variation within the Uralic language family. The interactive database built on these datasets is available at https://uralic.clld.org.

## How to cite the UraTyp dataset

If you use the data of the UraTyp database, please cite the dataset as

> Norvik, Miina, Yingqi Jing, Michael Dunn, Robert Forkel, Terhi Honkola, Gerson Klumpp, Richard Kowalik, Helle Metslang, Karl Pajusalu, Minerva Piha, Eva Saar, Sirkka Saarinen, & Outi Vesakoski. 2021. Uralic Typological database - UraTyp. Zenodo. https://doi.org/10.5281/zenodo.5236365

as well as the paper introducing it

> Norvik, Miina, Yingqi Jing, Michael Dunn, Robert Forkel, Terhi Honkola, Gerson Klumpp, Richard Kowalik, Helle Metslang, Karl Pajusalu, Minerva Piha, Eva Saar, Sirkka Saarinen, & Outi Vesakoski. 2022. Uralic typology in the light of a new comprehensive dataset. Journal of Uralic Linguistics 1(1): 4-42. https://doi.org/10.1075/jul.00002.nor

# Overview

Building the UraTyp database and developing the UT list of features has its origins in the typology dataset compiled by the research initiative BELDAN (Biological Evolution and the Diversification of Languages, www.bedlan.net) using seed money allocated by the Kone Foundation in 2013. The actual work with the UraTyp database started in 2018 within the framework of the project Kipot ja kielet ‘Pots and languages’ (funded by the University of Turku in 2018–2020) as a joint initiative between the University of Turku, University of Tartu, and Uppsala University. It also involved cooperation with the global Grambank initiative since the UT list of features was meant to supplement the GB list of features. The latter was developed at the Department of Cultural and Linguistic Evolution at the Max Planck Institute for the Science of Human History and at the Max Planck Institute for Evolutionary Anthropology. In order to make the two datasets compatible, cooperation also meant following the general principles of feature development and data collection used by the Grambank team.

The process of developing the UT list of features and collecting the data was coordinated by Miina Norvik. The features were designed and managed by Gerson Klumpp, Helle Metslang, Miina Norvik, Karl Pajusalu, and Eva Saar. The GB principles were introduced by Harald Hammarström and Michael Dunn. Feedback for the UT questionnaire was provided by Jeremy Bradley and Ksenia Shagal. The UT questions were coded by Miina Norvik, Minerva Piha, and Eva Saar. The GB part of the Uralic data was mainly collected by Richard Kowalik, and partly also by Miina Norvik; this data has also been contributed to the Grambank. Both the UT as well as GB features were coded by interviewing language experts (see the table below) and using literary sources (see `sources.bib`). In the case the information was obtained only from literary sources the respective information is included in the brackets. The following table also shows which languages are currently represented in the dataset and whether the UT and GB parts of the dataset have both been collected. 

Majority of the 360 features are formed as binary questions designed to be answered with “yes, this function/feature is present in the language” or “no, this function/feature is not present in the language”; some features in the GB dataset also allow for three options. The tables contain the following values: 0, 1 (in the case of multistate: 1, 2, 3), ? (answer not known), and N/A (not applicable).

In order to ensure consistency while coding, each feature was provided with a general description and a comment about what should be considered when coding a particular feature. For instance, as regards foreign influence there are comments saying that very recent foreign influence should not be considered. This and other kind of additional information can be find in the `doc` folder and it is also included in the interactive database available at https://uralic.clld.org/. 

Any grammar or data source  inherently reflects a certain linguistic variety, including with respect to time/a chronolect. In the case of modern standard languages, the goal was to code the standard varierty but if something was very prominent in the spoken language, this was also considered. As regards Uralic languages that are not in active every-day use anymore (e.g. Ingrian), have gone extinct (e.g. Kamas) or have no literary standard but exist in the form of several dialects (e.g. Ludian), we chose one particular language variety and considered what is/was characteristic or more widely spread in it. In some instances, this meant coding the language of the mid-20th century. 

The UT datasets also include examples whenever a feature was coded as 1 'yes, present'. The examples were usually added by the language expert, or by the coder and afterwards checked with the language expert. The examples originate from various kinds of sources: grammar books or sketches, language corpora, research articles, text collections; in the case the language expert was a native speaker, constructed examples were also allowed. Examples illustrating morphological or syntactic features come with glosses, while phonological characteristics are represented using the International Phonetic Alphabet. 

# Contents
The raw version of the dataset (found in the **`raw`** folder of the repository) is organized into folders and tables; the data structure is described in detail below. All tables are provided as CSV (comma-separated values) files.

### `UT`

This folder contains files that constitute the UT part of the UraTyp.<br/>
1. `Features.csv`<br/> 
Includes features, i.e. questions used to collect the UT data. The first column provides the feature ID, the second one includes the feature, and the third column specifies the broader area (phonology, morphology, syntax, or lexicon) under which the feature can be subsumed. Detailed descriptions of features can be found in the `doc` folder. Each description also contains information on what was considered when coding the respective feature.

2. `Finaldata.csv`<br/>
Presents all the data collected using the UT questionnaire in one table. It includes the names of the languages, their subfamilies, and the values (answers) for each feature (represented only by question ID).

3. `language-tables`<br/>
For each language, this folder contains a general table with values and a separate table with examples. The information in general tables is organized as follows:<br/>
(i) `ID` of the feature<br/>
(ii) `Name`of the feature<br/> 
(iii) Value for a particular language, i.e. the answer represented as 1 'yes, present', 0 'no, absent', ? 'no information', or N/A 'not applicable'<br/>
(iv) `Source` of information. The literary sources used to answer the questionnaire are included in the BibTeX file `sources.bib` in the **`raw`** folder. Whenever the information as regards the value (1 or 0), example, or a comment came from the language expert, the source column contains the name of the language expert.<br/>
(v) `Example` is given whenever the answer is 1 'yes, present'. The examples falling in the area of morphology or syntax are provided with glosses, while phonological examples are provided with the International Phonetic Alphabet. The linguistic examples are included in separate files titled according to the language names. <br/>
(vi) `Comment` is provided whenever necessary.


### `GB`

This folder includes the data collected using the GB questionnaire. 

1. `Features.csv`<br/>
Includes features used to collect the GB data. 

2. `Finaldata.csv`<br/>
Presents all the data collected using the GB questionnaire as one table. 

3. `language-tables`<br/>
For each language, this folder contains a general table with values provided for the GB questionnaire and a table with examples. The organiszation of the information in the tables is similar to that of the UT tables described above: (i) `ID`, (ii) `Feature`, (iii) `Value`, (iv) `Source`, (v) `Comment`, (vi) `Example`

### `gb.csv`
This file in the **`raw`** folder provides possible values for the GB questions.

### `Languages.csv`

This file contains information on the languages from where the data was collected (using the UT questionnaire and/or GB questionnaire). The table includes the names of the languages, their subfamilies, Glottocodes, ISO language codes, latitudes and longitudes, and also the sources used for a particular language to answer the question. 

### `sources.bib`

This file includes literary sources used to code the answers and provide examples.   

# Funders and supporters
SumuraSyyni (2014-2016) and AikaSyyni (2017-2021) funded by the Kone Foundation for Outi Vesakoski and UraLex (2014-2016) for Unni-Päivi Leino; Kipot ja kielet (2018-2020) funded by the University of Turku for Päivi Onkamo; URKO (Uralilainen Kolmio = ‘Uralic Triangle’ 2020-2022) funded by the Academy of Finland for Sirkka Saarinen, Päivi Onkamo and Harri Tolvanen; The Collegium for Transdisciplinary Studies in Archeology, Genetics and Linguistics, University of Tartu (2018–); Nikolai, Gerda, and Kadri Rõuk (2022-2024)

# Terms of use

This dataset is licensed under a CC-BY-4.0 license

Available online at https://github.com/cldf-datasets/uratyp
