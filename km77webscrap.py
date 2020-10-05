class km77webscrap:
    
    def __init__(self):
        pass
    
    def ScrapBrands(self):
        #Url donde se encuentra el listado de marcas
        url = 'https://www.km77.com/coches'
        #Header para simular un navegador
        headers = {'User-Agent': 
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        #Realizamos el request a la página
        readBrands = requests.get(url, headers=headers).text

        #Buscamos todos los elementos <a> que pueden contener links
        soup = BeautifulSoup(readBrands,'lxml')
        all_links = soup.find_all('a')

        #La siguente cabecera es la que diferencia los links a fabricantes de coches
        header = '/coches/'

        #De todos los elementos <a>, se queda con los links a los fabricantes y extrae el nombre
        links, brands = [], []
        for link in all_links:
            extracted = link.get('href')
            if not extracted == None:
                if extracted[0:(len(header))] == header:
                    extracted = 'https://www.km77.com' + extracted
                    links.append(extracted)
                    words = extracted.split('/')
                    words[-1] = words[-1].replace('-',' ')
                    words[-1] = words[-1].capitalize()
                    brands.append(words[-1])

        #Borramos un enlace que hace referencia a lanzamientos futuros
        links.remove('https://www.km77.com/coches/proximos-lanzamientos')
        brands.remove('Proximos lanzamientos')

        #Pasamos la lista a dataframe y grabamos el csv
        df_brands = pd.DataFrame(data={'Name': brands, 'Links': links})
        df_brands.to_csv('brands_links.csv', index=False)
    
    def LoadBrands(self):
        df_brands = pd.read_csv('brands_links.csv')
        return df_brands
    
    def ScrapModels(self, brands):
        #Header para simular un navegador
        headers = {'User-Agent': 
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        brand_l, link_l = [], []
        for i,r in brands.iterrows():
            brand = r[0]
            url = r[1]
            
            #Realizamos el request a la página
            readModels = requests.get(url, headers=headers).text

            #Buscamos todos los elementos <a> que pueden contener links
            soup = BeautifulSoup(readModels,'lxml')
            all_links = soup.find_all('a')

            #Para diferenciar las url porque tienen el formato xxx/coches/abarth/595/2016/estandar/datos
            tail = '/datos'

            #De todos los elementos <a>, se queda con los links a los modelos
            for link in all_links:
                extracted = link.get('href')
                if not extracted == None:
                    if extracted[(0-len(tail)):] == tail:
                        extracted = 'https://www.km77.com' + extracted
                        link_l.append(extracted)
                        brand_l.append(brand)

            #Pasamos la lista a dataframe 
            df_models = pd.DataFrame(data={'Brand': brand_l, 'Model link': link_l})
            df_models.to_csv('models_links.csv', index=False)

    def LoadModels(self):
        df_models = pd.read_csv('models_links.csv')
        return df_models
    
    def ScrapVersions(self, models):
        #Header para simular un navegador
        headers = {'User-Agent': 
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        brand_l, model_l, link_l = [], [], []
        for i,r in models.iterrows():
            brand = r[0]
            url = r[1]
            
            #Realizamos el request a la página
            readVersions = requests.get(url, headers=headers).text
            soup = BeautifulSoup(readVersions,'lxml')

            #El contenido que queremos está dentro de una tabla, la index 0
            all_tables = soup.find_all('table')
            tab = str(all_tables[0])
            souplink = BeautifulSoup(tab,'lxml')
            all_links = souplink.find_all('a')

            #Para copiar el hipervínculo de la versión
            for link in all_links:
                extracted = link.get('href')
                if not extracted == None:
                    extracted = 'https://www.km77.com' + extracted
                    name = extracted.split('/')[-2]
                    name = name.replace('-',' ')
                    name = name.capitalize()
                    
                    link_l.append(extracted)
                    model_l.append(name)
                    brand_l.append(brand)
                    
        #Pasamos la lista a dataframe 
        df_versions = pd.DataFrame(data={'Brand': brand_l, 'Version': model_l, 'Version link': link_l})
        df_versions.to_csv('versions_links.csv', index=False)
            
    def LoadVersions(self):
        df_versions = pd.read_csv('versions_links.csv')
        return df_versions
    
    def ScrapData(self, versions):
        #Header para simular un navegador
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        
        #Creamos un dataframe para almacenar todos los datos extraídos
        df_cars = pd.DataFrame(columns={'Marca','Versión','Precio','Potencia (CV)','Par (Nm)','Aceleración 0-100',
                                'Consumo l/100km','Emisiones CO2 g/km','Tracción','Caja de cambios','Tipo de carrocería',
                                'Longitud','Ancho','Alto','Peso'}) 
        brand_l, model_l, link_l = [], [], []
        
        #Iteramos sobre el listado de versiones y sus links
        for i,r in versions.iterrows():
            brand = r[0]
            model = r[1]
            url = r[2]

            
            #Realizamos el request a la página
            readData = requests.get(url, headers=headers).text
            soup = BeautifulSoup(readData,'lxml')
            
            #Pasamos todas las tablas a un dataframe. La última se elimina porque no aplica su información
            all_tables = soup.find_all('table')
            df = pd.DataFrame()
            for j in range(0,len(all_tables)-1):
                tab = str(all_tables[j])
                list_data = pd.read_html(tab)
                df_table = list_data[0]
                if len(df_table.columns) > 2:
                    df_table.drop(df_table.columns[[2]], axis=1, inplace=True)
                df = df.append(df_table, sort=True, ignore_index=True)
            
            df_temp = self.extract(brand, model, df)
            df_cars = df_cars.append(df_temp, ignore_index=True)
        
        #Forzamos que el dataframe esté ordenado tal y como queremos
        df_cars = df_cars[['Marca','Versión','Precio','Potencia (CV)','Par (Nm)','Aceleración 0-100',
                                'Consumo l/100km','Emisiones CO2 g/km','Tracción','Caja de cambios','Tipo de carrocería',
                                'Longitud','Ancho','Alto','Peso']]
        #Grabamos los datos como csv
        df_cars.to_csv('car_data.csv', index=False)
        
    def LoadData(self):
        df_cars = pd.read_csv('car_data.csv')
        return df_cars
        
    def extract(self, brand, model, df):
        #EXTRAEMOS LA INFORMACIÓN QUE NOS INTERESA (SE PUEDE AMPLIAR O REDUCIR)
        prices,accelerations,wltps,co2s,categories,longs,wides,heights,weights,cvs,nms,wheeldrives,gearboxes=[],[],[],[],[],[],[],[],[],[],[],[],[]
        #Extraemos el precio
        try:
            prices.append(float(df[1][0].split(' ')[0].replace('.','')))
        except:
            prices.append(float('NaN'))

        #Extraemos aceleracion
        try:
            accelerations.append(float(df[1][df[0]=='Aceleración 0-100 km/h'].iloc[0].split(' ')[0].replace(',','.')))
        except:
            accelerations.append(float('NaN'))

        #Extraemos consumo
        try:
            wltps.append(float(df[1][df[0]=='Combinado'].iloc[0].split(' ')[0].replace(',','.')))
        except:
            wltps.append(float('NaN'))

        #Extraemos emisiones
        try:
            co2s.append(float(df[1][df[0]=='Emisiones de CO2 WLTP'].iloc[0].split(' ')[0]))
        except:
            co2s.append(float('NaN'))

        #Extraemos carrocería
        try:
            categories.append(df[1][df[0]=='Tipo de Carrocería'].iloc[0])
        except:
            categories.append('NaN')

        #Extraemos longitud
        try:
            longs.append(float(df[1][df[0]=='Longitud'].iloc[0].split(' ')[0]))
        except:
            longs.append(float('NaN'))

        #Extraemos ancho
        try:
            wides.append(float(df[1][df[0]=='Anchura'].iloc[0].split(' ')[0]))
        except:
            wides.append(float('NaN'))

        #Extraemos altura
        try:
            heights.append(float(df[1][df[0]=='Altura'].iloc[0].split(' ')[0]))
        except:
            heights.append(float('NaN'))

        #Extraemos peso
        try:
            weights.append(float(df[1][df[0]=='Peso'].iloc[0].split(' ')[0].replace('.','')))
        except:
            weights.append(float('NaN'))

        #Extraemos potencia
        try:
            cvs.append(float(df[1][df[0]=='Potencia máxima'].iloc[0].split(' ')[0]))
        except:
            cvs.append(float('NaN'))

        #Extraemos par
        try:
            nms.append(float(df[1][df[0]=='Par máximo'].iloc[0].split(' ')[0]))
        except:
            nms.append(float('NaN'))

        #Extraemos tracción
        try:
            wheeldrives.append(df[1][df[0]=='Tracción'].iloc[0])
        except:
            wheeldrives.append('NaN')

        #Extraemos caja de cambios
        try:
            gearboxes.append(df[1][df[0]=='Caja de cambios'].iloc[0])
        except:
            gearboxes.append('NaN')
                
        df_temp = pd.DataFrame({'Marca':brand,
                                        'Versión':model,
                                        'Precio':prices, 
                                        'Potencia (CV)':cvs,
                                        'Par (Nm)':nms,
                                        'Aceleración 0-100':accelerations,
                                        'Consumo l/100km':wltps,
                                        'Emisiones CO2 g/km':co2s,
                                        'Tracción':wheeldrives,
                                        'Caja de cambios':gearboxes,
                                        'Tipo de carrocería':categories,
                                        'Longitud':longs,
                                        'Ancho':wides,
                                        'Alto':heights,
                                        'Peso':weights})     
        return df_temp