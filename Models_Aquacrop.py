#Este es un ejemplo de como utilizar AQUACROP

#instalar aquacrop 
# chekeamos que este instalado
!pip install aquacrop
# Si no esta instalado usamos
#pip install aquacrop
# Importamos desde aquacrop el generador del modelo, Suelo, Campo y condiciones iniciales
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
# Utilidades
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargamos el archivo donde se encuentran 
# En este caso utilizamos como ejemplo el archivo que viene incluido
filepath=get_filepath('tunis_climate.txt')
weather_data = prepare_weather(filepath)
weather_data

#Escogemos el tipo de suelo
sandy_loam = Soil(soil_type='SandyLoam')
#Typo de cultivo 
wheat = Crop('Wheat', planting_date='10/01')
#Condiciones iniciales de agua en el suelo al iniciar la simulacion
InitWC = InitialWaterContent(value=['FC']) # FC = Field capacity

#Creamos el modelo
model = AquaCropModel(sim_start_time=f'{1979}/10/01',
                      sim_end_time=f'{1985}/05/30',
                      weather_df=weather_data,
                      soil=sandy_loam,
                      crop=wheat,
                      initial_water_content=InitWC)
# Ejecutamos el modelo hasta el final de la simulacion
model.run_model(till_termination=True)

# Resultado de la simulacion del primer modelo 
model._outputs.water_flux.head()
model._outputs.water_storage.head()
model._outputs.crop_growth.head()
model._outputs.final_stats.head()


# Modelo 2 con diferente tipo de suelo 
# combine into aquacrop model and specify start and end simulation date
model_clay = AquaCropModel(sim_start_time=f'{1979}/10/01',
                      sim_end_time=f'{1985}/05/30',
                      weather_df=weather_data,
                      soil=Soil('Clay'),
                      crop=wheat,
                      initial_water_content=InitWC)

model_clay.run_model(till_termination=True)

###### GRAFICOS ##################
# Nombres
names=['Sandy Loam','Clay']
# Combinar los 2 modelos en una dataframe
dflist=[model._outputs.final_stats,
        model_clay._outputs.final_stats] 
# inicializamos la variable para guardar los resultados 
outlist=[]
for i in range(len(dflist)): # Leemos los datos de salida 
    temp = pd.DataFrame(dflist[i]['Yield (tonne/ha)']) # Tomamos el valor de toneladas por hectareas
    temp['label']=names[i] # Agregamos la etiqueta del tipo de suelo 
    outlist.append(temp) # Guardar los resultados en la variable que inicializamos antes
# Combinamos los resultados
all_outputs = pd.concat(outlist,axis=0)

###### GRAFICOS ######
# Nombres
names=['Sandy Loam','Clay']
# Combinar los 2 modelos en una dataframe
dflist=[model._outputs.final_stats,
        model_clay._outputs.final_stats] 
# inicializamos la variable para guardar los resultados 
outlist=[]
for i in range(len(dflist)): # Leemos los datos de salida 
    temp = pd.DataFrame(dflist[i]['Yield (tonne/ha)']) # Tomamos el valor de toneladas por hectareas
    temp['label']=names[i] # Agregamos la etiqueta del tipo de suelo 
    outlist.append(temp) # Guardar los resultados en la variable que inicializamos antes
# Combinamos los resultados
all_outputs = pd.concat(outlist,axis=0)
#create figure
fig,ax=plt.subplots(1,1,figsize=(10,7),)

# create box plot
sns.boxplot(data=all_outputs,x='label',y='Yield (tonne/ha)',ax=ax,)

# labels and font sizes
ax.tick_params(labelsize=15)
ax.set_xlabel(' ')
ax.set_ylabel('Yield (tonne/ha)',fontsize=18)



