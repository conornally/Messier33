import numpy as np
import Messier33
from Messier33.src.database import DataBase
from astropy.coordinates import SkyCoord
import astropy.units as u
from dustmaps.sfd import SFDQuery

class Catalog(DataBase):
    def __init__(self, data, style="null", name="null", indices={}, units="deg", history=[], bands=[]):
        self.style=style
        self.units=units
        super(Catalog,self).__init__(data,indices=indices, history=history, name=name, bands=bands)

        if(style=="pandas"): self.config=Messier33.pandas_config
        elif(style=="wfcam"): self.config=Messier33.wfcam_config

    @classmethod
    def from_dict(cls, raw_dict):
        return(cls(  data=raw_dict["data"],
                    style=raw_dict["style"],
                    indices=raw_dict["indices"], 
                    units=raw_dict["units"],
                    history=raw_dict["history"]))

    @classmethod
    def from_pandas(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_raw(filename, style="pandas"))
        cls.name=filename.split('/')[-1]
        return cls
    
    @classmethod
    def from_wfcam(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_raw(filename, style="wfcam"))
        cls.name=filename.split('/')[-1]
        return cls

    @classmethod
    def from_serialised(cls, filename):
        cls=cls.from_dict(Messier33.io.import_from_serialised(filename))
        cls.name=filename.split('/')[-1]
        return cls

    
    def convert_to_stdcoords(self, A=0, D=0):
        Messier33.info("*Converting RADEC to Standard Coordinates\n")
        if(not A):A=Messier33.ra
        if(not D):D=Messier33.dec
        if(self.units=="deg"):
            self['ra'] = np.radians(self['ra'])
            self['dec'] = np.radians(self['dec'])
            self.units="rads"
        if(self.units=="rads"):
            #for now this overwrites the ra/dec column, can change this if needed
            xi = (np.cos(self['dec'])*np.sin(self['ra']-A))/( np.sin(D)*np.sin(self['dec'])+np.cos(D)*np.cos(self['dec'])*np.cos(self['ra']-A))
            eta= (np.cos(D)*np.sin(self['dec'])-np.sin(D)*np.cos(self['dec'])*np.cos(self['ra']-A))/(np.sin(D)*np.sin(self['dec'])+np.cos(D)*np.cos(self['dec'])*np.cos(self['ra']-A))
            self.units="stdcoord"
            self.append(np.degrees(xi), "xi")
            self.append(np.degrees(eta), "eta")
        self.history.append("Converted RADEC to STDCoordinates")

    def deproject_radii(self):
        #not sure best interface, should i add to data, or create a new thing, or just return it
        #Cioni09.3 - 2.3
        Messier33.info("*Deprojecting radii\n")
        Q = Messier33.PA - np.radians(90)
        #Q = np.radians(90)- Messier33.PA
        _x = self['xi']*np.cos(Q) + self['eta']*np.sin(Q)
        _y = -self['xi']*np.sin(Q) + self['eta']*np.cos(Q)
        _y /= np.cos(Messier33.inclination)
        self.append(np.sqrt( _x**2.0 + _y**2.0) ,key="dist")
        self.history.append("Deprojected Radii from galactic centre")
        return(self['dist'])

    def projected_radii(self, ra, dec, unit="deg"):
        """
        INPUT:  ra,dec of origin
                unit = unit of ra and dec (deg,rads)
        FUNC:   creates column "dist" with these values
        """
        Messier33.info("*Calculating projected radii from (%f %f)\n"%(ra,dec))
        Messier33.warn("\x1b[31mThis funciton is overwriting column 'dist'\n\x1b[0m")
        if(unit not in ("deg","rads")): raise ValueError("unit must be 'deg' or 'rads', not '%s'"%unit)
        if((self.units=="rads") and (unit=="deg")):
            ra=np.radians(ra); dec=np.radians(dec)
            Messier33.debug("**Converting input units to radians\n")
        elif((self.units=="deg") and (unit=="rads")):
            ra=np.degrees(ra); dec=n.degrees(dec)
            Messier33.debug("**Converting input units to degrees\n")
        data= np.sqrt( (ra-self["ra"])**2.0 + (dec-self["dec"])**2.0 )
        if("dist" not in self.indices): self.append(data, "dist")
        else: self["dist"]=data


    def extinction_correct(self, overwrite=False):
        """
        INPUT:  overwrite (True) filter mag column with corrected magnitudes
        FUNC:   using SFDQuery finds E(B-V) for each ra,dec in catalog and 
                corrects the filter magnitudes using this value
        """
        Messier33.info("*Correcting Dust Extinction\n")
        coords = SkyCoord(self['ra'], self['dec'], unit=u.deg)
        ebv = SFDQuery()(coords)
        for band in self.bands:
            Messier33.info("**R_%s=%.4f (%s)\n"%(band, self.config.Rv3_1[band], self.config.Rv3_1['ref']))
            o = self[band] - (self.config.Rv3_1[band]*ebv)
            self.append(o, key="%so"%band)
            self.indices["d%so"%band]=self.indices["d%s"%band]
            if(overwrite): self.delete(band)
        self.history.append("Extinction Correction in bands %s"%self.bands)

    def apply_distance_modulus(self, d1, d2=10):
        """
        INPUT:  d1=current distance of sources [pc]
                d2=new distance of sources (default to 10pc
                #might just make this always true #overwrite (True) overwrites each magnitude band
        FUNC:   scales apparent magnitudes to appear as though they were at d2
                m2 = m1 - 5log10(d1/d2)
        """
        Messier33.info("Scaling distance from %f --> %f\n"%(d1,d2))
        dist_modulus = 5*np.log10(d1/d2)
        print(dist_modulus)
        for band in self.bands:
            self.replace(self[band]-dist_modulus, band)
            if("%so"%band in self.indices): self.replace(self["%so"%band]-dist_modulus, "%so"%band)
        self.history.append("Moved galactic distance from %f to %f updating magnitudes by %f"%(d1,d2, dist_modulus))

    def remove_nonstellar(self):
        Messier33.info("*Removing non-stellar sources from catalog\n")
        for band in self.bands:
            mask = Messier33.mask.Bool([-1,-2], "%scls"%band)
            self = mask.apply_on(self, overwrite=True)
        self.history.append("Removed any non-stellar sources from catalog")


if __name__=="__main__":
    Messier33.log_level=3
    data=[[0,0],[0,0]]
    indices={'x':0,'y':0}
    c=Catalog(data,indices)
    c2=c.copy(c)
