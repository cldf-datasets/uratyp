<a name="ds-structuredatasetmetadatajson"> </a>

# StructureDataset Uralic Typological database - UraTyp

**CLDF Metadata**: [StructureDataset-metadata.json](./StructureDataset-metadata.json)

**Sources**: [sources.bib](./sources.bib)

# Uralic Areal Typology Online (UraTyp) 2.0

The UraTyp 2.0 dataset includes information on 353 linguistic features spanning the domains of morphology, syntax, phonology, and, to a lesser extent, the lexicon. The data have been collected from all branches of the Uralic language family. The features are formulated as yes/no questions. Of the 353 features, 195 were answered using the Grambank questionnaire (i.e., the GB list of features), which was developed by the Grambank team to gather data from about half of the world’s languages (see https://grambank.clld.org/). The GB list of features and the development of the dataset are described in Skirgård et al. (2023). The remaining 158 features (i.e., the UT list of features) have been developed by the UraTyp author team to further investigate variation within the Uralic language family. The interactive database built on these datasets is available at https://uralic.clld.org/.

## How to cite the UraTyp 2.0 dataset

If you use the UraTyp 2.0 data, please cite the dataset as follows:<br/>
 
> Miina Norvik, Robert Forkel, Uldis Balodis, Jeremy Bradley, Michael Dunn, Ilya Egorov, Idaliia Feodotova, Terhi Honkola, Atte Huhtala, Yingqi Jing, Markus Juutinen, Olle Kejonen, Gerson Klumpp, Richard Kowalik, Nikolay Kuznetsov, Miika Lehtinen, Helle Metslang, Merit Niinemägi, Karl Pajusalu, Minerva Piha, Przemysław Podleśny, Mihkel Rünkla, Eva Saar, Sirkka Saarinen, Denys Teptiuk, Pire Teras, Marili Tomingas, Tuuli Tuisk, Janek Vaab, & Outi Vesakoski. (2026). Uralic Typological database - UraTyp (v2.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5236365

## Overview

Building the UraTyp database and developing the UT list of features has its origins in the typology dataset compiled by the research initiative BEDLAN (Biological Evolution and the Diversification of Languages, www.bedlan.net) using seed money provided by the Kone Foundation in 2013. The actual work on the UraTyp database began in 2018 within the framework of the project *Kipot ja kielet* ‘Pots and languages’ (funded by the University of Turku in 2018–2020), a joint initiative between the University of Turku, University of Tartu, and Uppsala University. The process of developing the UT list of features and collecting the data was coordinated by Miina Norvik. The features were originally designed and managed by Gerson Klumpp, Helle Metslang, Miina Norvik, Karl Pajusalu, and Eva Saar. Feedback on the UT questionnaire was provided by Jeremy Bradley and Ksenia Shagal. The work also involved collaboration with the global Grambank initiative, as the UT list of features was intended to supplement the GB list of features. The latter was developed at the Department of Cultural and Linguistic Evolution at the Max Planck Institute for the Science of Human History and at the Max Planck Institute for Evolutionary Anthropology. To ensure the compatibility of the two datasets, this collaboration also required adherence to the general principles of feature development and data collection established by the Grambank team. The GB principles were introduced by Harald Hammarström and Michael Dunn. 

**UraTyp 2.0** is a refined and updated version of UraTyp 1.0. The work has been primarily supported by the Nikolai, Gerda, and Kadri Rõuk Legacy Fund (2022-2024) and by Grant PRG2184 allocated by the Estonian Research Council (2024-2028). The preparations for UraTyp 2.0 involved revising the values and comments, providing examples for the GB part, and adding new languages. The UT questions were also refined: seven questions were removed, and those that underwent more substantial changes were assigned new numbers (UT200–UT205). The work additionally meant replacing p.c.-s (initially, many values were based on interviews with language experts) with references to published sources (see `sources.bib`). Nevertheless, consultation with researchers of the respective languages remained necessary. During the years, many contributors participated in checking the tables and providing examples and references (see `contributors.md`); all the work was coordinated by Miina Norvik. The GB part has also been submitted to Grambank.

The majority of the 353 features are formulated as questions designed to be answered with “yes, this function/feature is present in the language” or “no, this function/feature is not present in the language”; some features in the GB dataset also allow for three options. The tables contain the following values: 0, 1 (in the case of multistate: 1, 2, 3) and ? (answer not known).

To ensure consistency during the coding process, each feature was provided with a general description and comments explaining the considerations relevant for coding that particular feature. All descriptions for the UT part can be found in the `doc` folder and they are also included in the interactive database available at https://uralic.clld.org/. The descriptions for the GB part can be found at https://grambank.clld.org/.

Any grammar or data source inherently reflects a certain linguistic variety, including with respect to time (a chronolect). In the case of modern standard languages, the goal was to code the standard variety, but if something was very prominent in the spoken language, this was also taken into account. For Uralic languages that are no longer in active everyday use (e.g., Ingrian), have become extinct (e.g., Kamas), or lack a literary standard and exist in several dialectal varieties (e.g., Ludian), we chose one particular variety and considered what was characteristic or more widely attested in it. In some cases, this meant coding the language as used in the mid‑20th century.

Most of the datasets include examples whenever a feature was coded as present. The examples were added either by the language expert or by the coder. These originate from various types of sources: grammar books or sketches, language corpora, research articles, and text collections; in cases where the language expert was a native speaker, constructed examples were also allowed. Examples illustrating morphological or syntactic features come with glosses, while phonological features are represented using the International Phonetic Alphabet. 

## Contents

The raw version of the dataset (found in the **`raw`** folder of the repository) is organized into folders and tables; the data structure is described in detail below. All tables are provided as CSV (comma-separated values) files.

### `UT`

This folder contains the files that make up the UT part of UraTyp.<br/>

1. `Features.csv`<br/> 
Includes features, i.e., the questions used to collect the UT data. The first column provides the feature ID, the second column presents the feature itself, and the third column specifies the broader area (phonology, morphology, syntax, or lexicon) under which the feature could be classified. Detailed descriptions of features can be found in the `doc` folder. Each description also contains information on the criteria used when coding the respective feature.

2. `language-tables`<br/>
For each language, this folder contains a general table with values and a separate table with examples. The information in the general tables is organized as follows:<br/>
(i) `ID` of the feature<br/>
(ii) `Name` of the feature<br/> 
(iii) Value for the language, i.e., the answer represented as 1 'yes, present', 0 'no, absent' or ? 'no information'<br/>
(iv) `Source` of information. The literary sources used to answer the questionnaire are included in the BibTeX file `sources.bib` in the **`raw`** folder. Whenever the information regarding the value (1 or 0), example, or a comment comes from the language expert, the source column contains the name of that expert.<br/>
(v) `Example` is provided whenever the answer is 1 'yes, present'. The examples that fall within the area of morphology or syntax are given with glosses, while phonological examples are provided using the International Phonetic Alphabet. The linguistic examples are included in separate files named according to the languages.<br/>
(vi) `Comment` is provided whenever necessary.


### `GB`

This folder contains the files that make up the GB part of UraTyp. 

1. `Features.csv`<br/>
Includes features, i.e., the questions used to collect the GB data.

2. `language-tables`<br/>
For each language, this folder contains a general table with the values provided for the GB questionnaire and a table with examples. The organization of the information in these tables is similar to that of the UT tables described above: (i) `ID`, (ii) `Feature`, (iii) `Value`, (iv) `Source`, (v) `Comment`, (vi) `Example`

### `Languages.csv`

This file contains information on the languages from which the data were collected (using the UT questionnaire and/or the GB questionnaire). The table includes the names of the languages, their subfamilies, Glottocodes, ISO language codes, latitudes and longitudes, as well as the sources used for each language to answer the questions.

### `List_of_glosses.csv`

Examples that fall within the domains of morphology or syntax are given with glosses. This file contains a list of the glosses used in the tables.

### `gb.csv`

This file provides the possible values for the GB questions.

### `sources.bib`

This file contains literary sources used to answer the questions and provide examples.   

## Funders and supporters
SumuraSyyni (2014-2016) and AikaSyyni (2017-2021) funded by the Kone Foundation for Outi Vesakoski and UraLex (2014-2016) for Unni-Päivi Leino; Kipot ja kielet (2018-2020) funded by the University of Turku for Päivi Onkamo; URKO (Uralilainen Kolmio = ‘Uralic Triangle’ 2020-2022) funded by the Academy of Finland for Sirkka Saarinen, Päivi Onkamo, and Harri Tolvanen; The Collegium for Transdisciplinary Studies in Archaeology, Genetics and Linguistics, University of Tartu (2018–); Nikolai, Gerda, and Kadri Rõuk Legacy Fund (2022-2024). PRG2184 “From East to West: Typological shift in Estonian and the Southern Finnic languages against the background of Uralic” (2024-2028), TK215 “Estonian Roots: Centre of Excellence for transdisciplinary studies on ethnogenesis and cultural diversity” (2024-2030).

## Providing feedback
If you would like to give feedback, please contact Miina Norvik (miina.norvik@ut.ee) or use `Issues` in GitHub.

## Terms of use

This dataset is licensed under a CC-BY-4.0 license

Available online at https://github.com/cldf-datasets/uratyp


property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Miina Norvik, Robert Forkel, Uldis Balodis, Jeremy Bradley, Michael Dunn, Ilya Egorov, Idaliia Feodotova, Terhi Honkola, Atte Huhtala, Yingqi Jing, Markus Juutinen, Olle Kejonen, Gerson Klumpp, Richard Kowalik, Nikolay Kuznetsov, Miika Lehtinen, Helle Metslang, Merit Niinemägi, Karl Pajusalu, Minerva Piha, Przemysław Podleśny, Mihkel Rünkla, Eva Saar, Sirkka Saarinen, Denys Teptiuk, Pire Teras, Marili Tomingas, Tuuli Tuisk, Janek Vaab, & Outi Vesakoski. (2026). Uralic Typological database - UraTyp (v2.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.5236365
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF StructureDataset](http://cldf.clld.org/v1.0/terms.rdf#StructureDataset)
[dc:identifier](http://purl.org/dc/terms/identifier) | https://uralic.clld.org
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/bedlan/uratyp-1
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/bedlan/uratyp-1/tree/b99fc33">bedlan/uratyp-1 b99fc33</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v5.3">Glottolog v5.3</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.12.3</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | uratyp
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-valuescsv"></a>Table [values.csv](./values.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ValueTable](http://cldf.clld.org/v1.0/terms.rdf#ValueTable)
[dc:extent](http://purl.org/dc/terms/extent) | 13414


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | References [parameters.csv::ID](#table-parameterscsv)
[Value](http://cldf.clld.org/v1.0/terms.rdf#value) | `string` | 
[Code_ID](http://cldf.clld.org/v1.0/terms.rdf#codeReference) | `string` | References [codes.csv::ID](#table-codescsv)
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Source_Comment` | `string` | 
[Example_ID](http://cldf.clld.org/v1.0/terms.rdf#exampleReference) | list of `string` (separated by ` `) | References [examples.csv::ID](#table-examplescsv)

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 39


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal`<br>&ge; -90<br>&le; 90 | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal`<br>&ge; -180<br>&le; 180 | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string`<br>Regex: `[a-z0-9]{4}[1-9][0-9]{3}` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string`<br>Regex: `[a-z]{3}` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`UT_Experts` | list of `string` (separated by ` `) | References [contributors.csv::ID](#table-contributorscsv)
`GB_Experts` | list of `string` (separated by ` `) | References [contributors.csv::ID](#table-contributorscsv)
`Subfamily` | `string` | 

## <a name="table-contributorscsv"></a>Table [contributors.csv](./contributors.csv)

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 56


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 

## <a name="table-codescsv"></a>Table [codes.csv](./codes.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF CodeTable](http://cldf.clld.org/v1.0/terms.rdf#CodeTable)
[dc:extent](http://purl.org/dc/terms/extent) | 714


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | The parameter or variable the code belongs to.<br>References [parameters.csv::ID](#table-parameterscsv)
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 

## <a name="table-examplescsv"></a>Table [examples.csv](./examples.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ExampleTable](http://cldf.clld.org/v1.0/terms.rdf#ExampleTable)
[dc:extent](http://purl.org/dc/terms/extent) | 5421


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | References [languages.csv::ID](#table-languagescsv)
[Primary_Text](http://cldf.clld.org/v1.0/terms.rdf#primaryText) | `string` | The example text in the source language.
[Analyzed_Word](http://cldf.clld.org/v1.0/terms.rdf#analyzedWord) | list of `string` (separated by `	`) | The sequence of words of the primary text to be aligned with glosses
[Gloss](http://cldf.clld.org/v1.0/terms.rdf#gloss) | list of `string` (separated by `	`) | The sequence of glosses aligned with the words of the primary text
[Translated_Text](http://cldf.clld.org/v1.0/terms.rdf#translatedText) | `string` | The translation of the example text in a meta language
[Meta_Language_ID](http://cldf.clld.org/v1.0/terms.rdf#metaLanguageReference) | `string` | References the language of the translated text<br>References [languages.csv::ID](#table-languagescsv)
[LGR_Conformance](http://cldf.clld.org/v1.0/terms.rdf#lgrConformance) | `string`<br>Valid choices:<br> `WORD_ALIGNED` `MORPHEME_ALIGNED` | The level of conformance of the example with the Leipzig Glossing Rules
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`IPA` | `string` | 

## <a name="table-contributionscsv"></a>Table [contributions.csv](./contributions.csv)

UraTyp combines typological data collected with two separate questionnaires. These questionnaires are listed in the ContributionTable, and parameters, i.e. features (and thus values) are linked to this table according to their origin.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 2


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[Contributor](http://cldf.clld.org/v1.0/terms.rdf#contributor) | `string` | 
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | 

## <a name="table-parameterscsv"></a>Table [parameters.csv](./parameters.csv)

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 353


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[ColumnSpec](http://cldf.clld.org/v1.0/terms.rdf#columnSpec) | `json` | 
`Area` | `string` | 
[Contribution_ID](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | `string` | Links a feature to the questionnaire it comes from.<br>References [contributions.csv::ID](#table-contributionscsv)
`Feature_Description` | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | Sources cited in the feature description.<br>References [sources.bib::BibTeX-key](./sources.bib)

