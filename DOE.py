import matplotlib as mpl
import matplotlib.pyplot as pyp
import pandas as pd
import seaborn as sbn
import scipy.interpolate as inter
from matplotlib import rc
#allows for latex text rendering disable if no version of TEX installed
rc('text',usetex = True)
#rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

def plastic_strain(stress,strain,E):
	elastic_strain = stress/E
	plastic_strain = strain - elastic_strain
	return plastic_strain

def get_E(stress,strain):
	E = (stress[1])/(strain[1])
	return E

def curves(trial,num,srf):
	trial['strain'] = trial['U']/20
	trial['stress'] = trial['RF']/20
	E = get_E(trial['stress'], trial['strain'])
	E1 = get_E(trial['stress'],trial['strain'])
	trial['PE'] = plastic_strain(trial['stress'],trial['strain'],E1)
	print(f"**************Trial{num}***************\n")
	strf = inter.interp1d(trial['strain'],trial['stress'])
	sigma_f = strf(srf)
	print(f'GLOBAL STRESS @ FAILURE:  {sigma_f}\n')
	pef = inter.interp1d(trial['strain'],trial['PE'])
	pe_f = pef(srf)
	print(f'PLASTIC STRAIN @ FAILURE: {pe_f}\n')
	return (sigma_f,pe_f,E);


doe = pd.read_excel("G:\My Drive\PLASTICDOE\DOEPLASTIC.xlsx")
print(doe)
eF = doe['e_F']
doe['bar'] = doe['Bond Width']/(10-doe['K'])
print(eF)
run = []	#run:
sigma = []	#sigma:
pe = []	
E = []
for i in range(1,10):
	c_t = pd.read_excel(f"G:\My Drive\PLASTICDOE\TRIAL {i}.xlsx")
	s,p,el = curves(c_t,i,eF[i-1])
	ind =  c_t[c_t['strain'].gt(eF[i-1])].index[0]
	print(ind)
	#removes invailid data
	c_t = c_t.truncate(after = ind)
	sigma.append(s)
	E.append(el)
	pe.append(p)
	run.append(c_t)
data = doe[['e_F','PE','F','Bond Width','Failure Stress','C','Order','bar']]
yellow = (data['Bond Width']-data['Bond Width'].min())/(data['Bond Width'].max()-data['Bond Width'].min());
green = (data['F']-data['F'].min())/(data['F'].max()-data['F'].min());
point_cols = []
for i in range(0,9):
    point_cols.append((yellow[i],0,green[i]))
    


print(point_cols)
pyp.xlabel('Porosity');
pyp.ylabel('Bond Width');
pyp.scatter(data['F'],data['Bond Width'],c = point_cols,s = 400)
pyp.show()
data['E'] = E
data['E'] = E
#sbn.set(style = 'ticks')
y_bin = ['e_F', 'PE' , 'Failure Stress', 'C', 'E']	#y_bin:
x_bin = ['bar','Bond Width', 'F']	#x_bin:
y_lab = ['$\epsilon_{ut}$', '$\epsilon_{plastic-ut}$' , '$\sigma_{ut} (Pa)$', '$K_{t}$','E (Pa)' ]	#y_lab: labels for y axis
x_lab = ['Bond Aspect Ratio','Bond Width (m)', 'Porosity']	#x_lab: labels for x axis'
fig,a = pyp.subplots(5,3)	#creates a matrix of plots 
ia = 0
for i in y_bin:
	ja = 0
	for j in x_bin:
			a[ia][ja].scatter(data[j],data[i],c = point_cols)
			a[ia][ja].set_xlabel(x_lab[ja])
			a[ia][ja].set_ylabel(y_lab[ia])
			ja = ja+1
	ia = ia + 1

for ax in a.flat:
	ax.label_outer()


pyp.ticklabel_format(style='sci', axis='x', scilimits=None)
fig.suptitle('Exploration of Bond Width and Porosity')
pyp.show()


fig2,axs = pyp.subplots(3,3,sharex=True, sharey = True)
num = 0;


cols = ['Bw = 0.1', 'Bw = 0.3', 'Bw = 0.5']	#cols: name for coloums
rows = ['f = 0.3', 'f = 0.2' , 'f  = 0.1']	#rows: name for rows 
for ax in axs.flat:
    dat = run[num]
    ax.plot(dat['strain'],dat['stress'],label = '$\sigma (MPa)$',linewidth = 2)
    ax.plot(dat['strain'],dat['strain'] * E[num],dashes = [1,2],label = '$E$', linewidth = 2)
    ax.hlines(sigma[num],dat['strain'].min(),dat['strain'].max(), label = '$\sigma_{ut}$',linewidth = 1)
    #axis title
    ax.set(xlabel = '$\epsilon$',ylabel = '$\sigma$')
    num = num + 1

#for ax in axs.flat:
    #ax.xlabel_outer()

#adds titles for rows & cols
for ax, col in zip(axs[0], cols):
    ax.set_title(col)

for ax, row in zip(axs[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')

axs[2][2].legend(loc = 'lower right')
pyp.show()

#pyp.plot(run['strain'],run['stress'])
#pyp.show()
