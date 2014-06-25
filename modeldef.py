import json
from sedpy import observate, attenuation
import elines, sedmodel, gp
from priors import tophat

rp = {'verbose':True,
      'filename':'data/mmt/nocal/020.B192-G242.s.fits',
      'objname': 'B192-G242',
      'wlo':3750., 'whi': 7200.,
      'ftol':0.5e-5, 'maxfev':50000, 'nsamplers':1,
      'walker_factor':8, 'nthreads':1, 'nburn':3 * [50], 'niter': 200, 'initial_disp':0.01
      }

parlist = []
parlist.append({'name': 'lumdist', 'N': 1,
                'isfree': False,
                'init': 0.783,
                'units': 'Mpc',
                'prior_function': None,
                'prior_args': None})

###### SFH ################

parlist.append({'name': 'mass', 'N': 1,
                'isfree': True,
                'init': 10e3,
                'units': r'M$_\odot$',
                'prior_function': tophat,
                'prior_args': {'mini':1e2, 'maxi': 1e6}})

parlist.append({'name': 'tage', 'N': 1,
                'isfree': True,
                'init': 0.250,
                'units': 'Gyr',
                'prior_function':tophat,
                'prior_args':{'mini':0.001, 'maxi':2.5}})

parlist.append({'name': 'zmet', 'N': 1,
                'isfree': True,
                'init': -0.2,
                'units:': r'$\log (Z/Z_\odot)$',
                'prior_function': tophat,
                'prior_args': {'mini':-1, 'maxi':0.19}})

parlist.append({'name': 'sfh', 'N':1,
                'isfree': False,
                'init': 0,
                'units': None})

###### DUST ##################

parlist.append({'name': 'dust_curve', 'N': 1,
                'isfree': False,
                'init': attenuation.cardelli,
                'units': None})

parlist.append({'name': 'dust2', 'N': 1,
                'isfree': True,
                'init': 0.5,
                'units': r'$\tau_V$',
                'prior_function': tophat,
                'prior_args': {'mini':0.0, 'maxi':2.5}})

parlist.append({'name': 'dust1', 'N': 1,
                'isfree': False,
                'init': 0.0,
                'units': r'$\tau_V$',
                'prior_function': None,
                'prior_args': None})

parlist.append({'name': 'dust_tesc', 'N': 1,
                'isfree': False,
                'init': 0.01,
                'units': 'Gyr',
                'prior_function': None,
                'prior_args': None})

parlist.append({'name': 'dust_type', 'N': 1,
                'isfree': False,
                'init': 1,
                'units': 'NOT USED'})

###### IMF ###################

parlist.append({'name': 'imf_type', 'N': 1,
                'isfree': False,
                'init': 2, #2 = kroupa
                'units': None})

parlist.append({'name': 'imf3', 'N':1,
                'isfree': False,
                'init': 2.3,
                'units': None,
                'prior_function':tophat,
                'prior_args':{'mini':1.3, 'maxi':3.5}})

###### WAVELENGTH SCALE ######

parlist.append({'name': 'zred', 'N':1,
                'isfree': True,
                'init': 0.00001,
                'units': None,
                'prior_function': tophat,
                'prior_args': {'mini':-0.001, 'maxi':0.001}})

parlist.append({'name': 'sigma_smooth', 'N': 1,
                'isfree': True,
                'init': 2.2,
                'units': r'$\AA$',
                'prior_function': tophat,
                'prior_args': {'mini':1.0, 'maxi':6.0}})

parlist.append({'name': 'smooth_velocity', 'N': 1,
                'isfree': False,
                'init': True,
                'units': None})

parlist.append({'name': 'min_wave_smooth', 'N': 1,
                'isfree': False,
                'init': 3700.0,
                'units': r'$\AA$'})

parlist.append({'name': 'max_wave_smooth', 'N': 1,
                'isfree': False,
                'init': 7300.0,
                'units': r'$\AA$'})

###### CALIBRATION ###########

polyorder = 2
polymin = [-5, -50]
polymax = [5, 50]
polyinit = [0.1, 0.1]

parlist.append({'name': 'poly_coeffs', 'N': polyorder,
                'isfree': True,
                'init': polyinit,
                'units': None,
                'prior_function': tophat,
                'prior_args': {'mini':polymin, 'maxi':polymax}})
    
parlist.append({'name': 'spec_norm', 'N':1,
                'isfree': True,
                'init':1,
                'units': None,
                'prior_function': tophat,
                'prior_args': {'mini':0.1, 'maxi':10}})

parlist.append({'name': 'gp_jitter', 'N':1,
                'isfree': True,
                'init': 0.,
                'units': 'spec units',
                'prior_function': tophat,
                'prior_args': {'mini':0.0, 'maxi':0.1}})

parlist.append({'name': 'gp_amplitude', 'N':1,
                'isfree': True,
                'init': 0.04,
                'units': 'spec units',
                'prior_function': tophat,
                'prior_args': {'mini':0.0, 'maxi':3}})

parlist.append({'name': 'gp_length', 'N':1,
                'isfree': True,
                'init': 50.0,
                'units': r'$\AA$',
                'prior_function': tophat,
                'prior_args': {'mini':20.0, 'maxi':200}})

parlist.append({'name': 'phot_jitter', 'N':1,
                'isfree': False,
                'init': 0.0,
                'units': 'maggies',
                'prior_function': tophat,
                'prior_args': {'mini':0.0, 'maxi':0.2}})

###### EMISSION ##############

linelist = ['CaII_K', 'NaI_5891', 'NaI_5897',
            'Ha', 'NII_6585','SII_6718','SII_6732',
            'HeI_3821','HeI_4010','HeI_4027','HeI_4145', 'HeI_4389','HeI_4473','HeI_4923','HeI_5017'
            ]
linemin = 3 * [-100] + 4 * [0.]  + 8 * [-50.0 ]
linemax = 3 * [0.] + 4 * [100.0 ] + 8 * [50.0 ]
lineinit = 3 * [-0.1 ] + 4 * [1.0 ] + 8 * [0.1 ]

nlines = len(linelist)
ewave = [elines.wavelength[l] for l in linelist]

parlist.append({'name': 'emission_rest_wavelengths', 'N': nlines,
                'isfree': False,
                'init': ewave,
                'line_names': linelist,
                'units': r'$\AA$'})

parlist.append({'name': 'emission_luminosity', 'N': nlines,
                'isfree': True,
                'init': lineinit,
                'units': r'$L_\odot$',
                'prior_function':tophat,
                'line_names': linelist,
                'prior_args':{'mini': linemin, 'maxi': linemax}})

parlist.append({'name': 'emission_disp', 'N': 1, 'isfree': True,
                'init': 2.2,
                'units': r'$\AA$',
                'prior_function':tophat,
                'prior_args':{'mini':1.0, 'maxi':6.0}})

#class NumpyAwareJSONEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, numpy.ndarray) and obj.ndim == 1:
#                return [x for x in obj]
#        return json.JSONEncoder.default(self, obj)

def write_plist(plist, runpars, filename):
    pass

def read_plist(filename):
#    return plist, runpars
    pass

def initialize_model(rp, plist, obs):    
    theta_desc, fixed_params  = {}, {}
    initial_theta = []
    count = 0
    for i, par in enumerate(plist):
        if par['isfree']:
            par['i0'] = count
            name = par.pop('name')
            theta_desc[name] = par
            count += par['N']
            #need to deal with iterables here
            try:
                n = len(par['init'])
            except:
                n =1
                v = [par['init']]
            else:
                v = par['init']
            if par['N'] != n:
                raise TypeError("Parameter value vector of "\
                                "{0} not same as declared size".format(name))
            # Finally, append this to the initial
            #  parameter vector
            initial_theta += v
        else:
            fixed_params[par['name']] = par['init']

    # SED Model
    model = sedmodel.SedModel(theta_desc = theta_desc, **fixed_params)
    model.add_obs(obs)
    model, initial_theta = norm_spectrum(model, initial_theta)
    model.ndof = len(model.obs['wavelength']) + len(model.obs['mags'])
    model.verbose = rp['verbose']

    #Add Gaussian Process
    mask = model.obs['mask']
    model.gp = gp.GaussianProcess(model.obs['wavelength'][mask],
                                  model.obs['unc'][mask])

    return model, initial_theta


def norm_spectrum(model, initial_center, band_name = 'f475w'):
    """
    Initial guess of spectral normalization using photometry.

    This multiplies the observed spectrum by the factor required
    to reproduce the photometry.  Default is to produce a spectrum
    that is approximately in erg/s/cm^2/AA (Lsun/AA/Mpc**2).
    """
    #use f475w for normalization
    norm_band = [i for i,f in enumerate(model.obs['filters'])
                 if band_name in f.name][0]
    
    synphot = observate.getSED(model.obs['wavelength'],
                               model.obs['spectrum'],
                               model.obs['filters'])

    # Factor by which model spectra should be multiplied to give you
    #  the photometry, using the F475W filter as truth
    norm = 10**(-0.4*(synphot[norm_band] - model.obs['mags'][norm_band]))
    model.params['normalization_guess'] = norm
    
    #model.obs['spectrum'] *= norm
    #model.obs['unc'] *= norm
    #model.obs['scale'] = model.obs.get('scale', 1.0) * norm
    
    # Assume you've got this right to within some factor after
    #  marginalized over everything that changes spectral shape within
    #  the band (polynomial terms, dust, age, etc)
    #fudge = (1 + 10 * model.obs['mags_unc'][norm_band]/1.086)
    fudge = 3.0
    model.theta_desc['spec_norm']['prior_args'] = {'mini':1 / fudge,
                                                   'maxi':fudge }

    # Pivot the polynomial near the filter used for approximate
    # normalization
    model.params['pivot_wave'] =  model.obs['filters'][norm_band].wave_effective 
    model.params['pivot_wave'] = 4750.
 
    initial_center[model.theta_desc['spec_norm']['i0']] = 1.0
 
    return model, initial_center

class Parameter(object):
    """
    For a possible switch from dictionaries to specialized objects for
    the parameters.  This would require a massive rewrite of
    ThetaParameters() and seems unnecessary, though a little cleaner
    and of cource more OO
    """
    def __init__(self, name, **kwargs):
        self.name = name
        self.prior_function = None
        self.prior_grad_function = None
        self.prior_args = {}
        self.isfree = False
        for k, v in kwargs.iteritems():
            setattr(self,k,v)

    def lnp_prior(self, theta):
        try:
            return self.prior_function(theta, **self.prior_args)
        except:
            return 0
        
    @property
    def N(self):
        try:
            return len(self.value)
        except TypeError:
            return 1

    @property
    def bounds(self):
        pass

    #@property
    #def isfree(self):
    #    return self.free
