# projet_DL_photoreceptor
projet universitaire de développement d'un outil de comptage de cellules photoréceptrices de drosophile.

# Setup 

### Clone le repos

```bash
# clone le repo
git clone git@github.com:tyrosine-rex/projet_DL_photoreceptor.git

# entre dans la racine du repos
cd projet_DL_photoreceptor
```

### Téléchargment des données 

```bash
# copie les images depuis pedago-ngs vers ./data/
scp -r pedago-ngs:/localdata/pandata/students/Projet_12_IA/data_img.tar.gz ./data/

# decompresse l'archive dans ./data/ vers ./data/
tar -xzf data/data_img.tar.gz -C ./data/
```

### Rangement des données

```bash
# range les images en fonction de leurs categories/nb d'ommatidies 
# usage :  MakeGroupFromVignettes [-h] -s SOURCE -d DESTINATION

./misc/MakeGroupFromVignettes.py -s ./data/data_img/vignettes_manu_annot -d ./data/vignettes_manu_tidy  
```

### Mise en place de l'environnement 

À venir 🤠





