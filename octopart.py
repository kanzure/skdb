#!/usr/bin/python
#an attempt at implementing the octopart api v2
#url: http://octopart.com/api/documentation
#skdb api key: 476188c7
import optfunc
import simplejson
import unittest
import pycurl
from urllib import urlencode
from StringIO import StringIO

octopart_api_key = "476188c7"
bryan_message = "bryan hasn't got this far yet"

class Octopart:
    '''a wrapper to Octopart.com'''
    timeout = 15 #dunno what to put here (seconds)
    base_url = "http://octopart.com/api/v2/"
    filters = "case_package, category_id, color, conductor_material, contact_material, contacts_type, dielectric_material, flammability_rating, gender, glow_wire_compliant, halogen_free_status, housing_color, housing_material, insulation_material, jacket_material, lead_free_status, lens_color, lens_type, lifecycle_status, logic_type, manufacturer, material, mounting_type, orientation, packaging, polarity, processor_type, rohs, shielding, shrouded, supplier, termination_style, thermal_shutdown"
    ranged_filters = "access_time, avg_authavail, avg_authprice, avg_avail, avg_price, breakdown_voltage, cable_length, capacitance, carry_current, character_size_height, clock_speed, coil_resistance, contact_resistance, cord_length, current_rating, data_rate, dropout_voltage, equivalent_series_resistance_esr, forward_voltage, frequency, gain, inductance, input_bias_current, input_current, input_power, input_voltage_dc, load_capacitance, luminous_intensity, mated_height, number_of_channels, number_of_circuits, number_of_conductors, number_of_detents, number_of_gates, number_of_i_o_pins, number_of_outlets, number_of_outputs, number_of_pins, number_of_positions, number_of_rows, operating_temperature, output_current, output_power, output_voltage, peak_wavelength, pin_pitch, power_consumption, power_rating, q_factor, quiescent_current, resistance, resistance_tolerance, sample_rate, size_diameter, size_height, size_inner_diameter, size_length, size_thickness, size_width, slew_rate, supply_voltage_dc, switching_current, switching_frequency, switching_voltage, temperature_coefficient, threshold_voltage, voltage_rating_ac, voltage_rating_dc, voltage_rating_transient, wavelength, weight"
    def __init__(self, api_key=None):
        self.api_key = api_key
    def web_fetch(self, url):
        buffer = StringIO()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.TIMEOUT, self.timeout)
        curl.setopt(curl.WRITEFUNCTION, buffer.write)
        curl.perform()
        curl.close()
        response = buffer.getvalue().strip()
        return response
    def get_categories(self, id=4179, attach_ancestors=0):
        if isinstance(id, list):
            specific_url = "categories/get_multi"
            #url: http://octopart.com/api/v2/categories/get_multi?ids=[5432,692,2344]
            id_variable = "ids"
        else: #it's just a single number
            specific_url = "categories/get"
            #url: http://octopart.com/api/v2/categories/get?id=533642
            id_variable = "id"
        
        id = str(id)
        attach_ancestors = str(attach_ancestors)

        url = self.base_url + specific_url + "?" + id_variable + "=" + id + "&attach_ancestors=" + attach_ancestors + "&apikey=" + self.api_key
        response_json = self.web_fetch(url)

        #results
        #The response is a list of category objects that match the ids requested.
        #If a match is not found for a given id, the response will not include that object.
        #In other words, if no categories are found the reponse will be an empty list.
        #raise NotImplementedError, bryan_message
        
        return simplejson.loads(response_json)
    def get_whitepapers(self, id):
        '''returns a whitepaper object
        id: the whitepaper object id'''
        if isinstance(id, list):
            specific_url = "whitepapers/get_multi"
            #url: http://octopart.com/api/v2/whitepapers/get_multi
            id_variable = "ids"
        else:
            specific_url = "whitepapers/get"
            #url: http://octopart.com/api/v2/whitepapers/get
            id_variable = "id"
        
        id = str(id)
        url = self.base_url + specific_url + "?" + id_variable + "=" + id
        response_json = self.web_fetch(url)

        #results
        #a whitepaper object
        #url: http://octopart.com/api/documentation#whitepaper

        return simplejson.loads(response_json)
    def search_categories(self, query="", start=0, limit=10, ancestor_id=None, attach_ancestors=0):
        '''query: query string (optional)
        start: ordinal position of the first result (default is 0)
        limit: maximum number of results to return (default is 10)
        ancestor_id: if specified, limit search to all descendants of the specified ancestor (optional)
        attach_ancestors: if specified, attach ancestors to category objects (optional)'''
        specific_url = "categories/search"
        
        if not ancestor_id: ancestor_id = ""
        if not attach_ancestors: anttach_ancestors = ""
        start = str(start)
        limit = str(limit)
        ancestor_id = str(ancestor_id)
        attach_ancestors = str(attach_ancestors)

        url = self.base_url + specific_url + "?" + "q=" + query + "&start=" + start + "&limit=" + limit + "&ancestor_id=" + ancestor_id + "&attach_ancestors=" + attach_ancestors + "&apikey=" + self.api_key
        response_json = self.web_fetch(url)

        #results
        #    * results[]{} - The sorted list of matched items
        #          o item{} - A matched category object
        #          o highlight - A short snippet of text highlighting matched keywords
        #    * request{} - The request parameters (from the arguments above)
        #          o q
        #          o start
        #          o limit
        #          o ancestor_id
        #    * hits - The total number of matched objects
        #    * time - The amount of time it took to process the entire request (in seconds)
        return simplejson.loads(response_json)
    def search_parts(self, query="", start=0, limit=10, filters=None, ranged_filters=None, sort_by=None):
        '''query: query string (optional)
        start: ordinal position of the first result (default is 0, max is 1000)
        limit: number of results to return (default is 10, maximum is 100)
        filter: JSON encoded list of (fieldname, values) pairs (optional)
            example: filters=[["color",["Red"]], ["material",["Tantalum","Ceramic"]]]
        ranged_filters: JSON encoded list of (fieldname, min/max values) pairs, using null as wildcard. (optional)
            example: ranged_filters=[["resistance",[[100,1000],[2000,null]]]]
        sort_by: JSON encoded list of (fieldname,sort-order) pairs, default is [["score","desc"]] (optional)
            example: sort_by=[["resistance","desc"],["avg_price","asc"]]'''
        specific_url = "parts/search"

        #some preliminary checks
        if start < 0: raise ValueError, "Octopart.search_parts: start must be greater than 0"
        if start > 1000: raise ValueError, "Octopart.search_parts: start must be less than or equal to 1000"
        if limit <= 0: limit = 100 #set it to the maximum
        if limit > 100: raise ValueError, "Octopart.search_parts: limit must be between 0 and 100 (inclusive)"
        if not query: query = ""
        if not filters: filters = ""
        if not ranged_filters: ranged_filters = ""
        if not sort_by: sort_by = ""

        start = str(start)
        limit = str(limit)

        url = self.base_url + specific_url + "?" + "q=" + query + "&start=" + start + "&apikey=" + self.api_key
        #do not include filters and rangedfilters if they aren't available
        if ranged_filters != "": url = url + "&rangedfilters=" + ranged_filters
        if filters != "": url = url + "&filters=" + filters
        if sort_by != "": url = url + "&sortby=" + sort_by
        
        response_json = self.web_fetch(url)
        response = simplejson.loads(response_json)
        
        #results
        #    *  results[]{} - The sorted list of matched items
        #          o item{} - A matched part object
        #          o highlight - A short snippet of text highlighting matched keywords
        #    * request{} - The request parameters (from the arguments above)
        #          o q
        #          o start
        #          o limit
        #          o filters
        #          o rangedfilters
        #          o sortby
        #    * hits - The total number of matched objects
        #    * time - The amount of time it took to process the entire request (in seconds)
        hits = response["hits"]
        time = response["time"] #in seconds

        for part in response["results"]:
            part = part["item"]
            specs = {}
            for attribute in part["specs"]:
                specs[attribute["attribute"]["fieldname"]] = attribute["values"]
            print "part id: ", part["id"]
            
            for spec in specs:
                print "\t" + spec + "\t" + str(specs[spec])

        return response
    def search_whitepapers(self, query="", start=0, limit=10):
        '''execute a search over all whitepapers
        query: query string (optional)
        start: ordinal position of the first result where the first position is 0 (default is 0, max is 1000) (optional)
        limit: maximum number of results to return (default is 10, max is 100) (optional)
        '''
        specific_url = "whitepapers/search"

        #some preliminary checks
        if start<0: raise ValueError, "Octopart.search_whitepapers: start must be greater than or equal to 0"
        if start>1000: raise ValueError, "Octopart.search_whitepapers: start must be less than or equal to 1000"
        start = str(start)
        limit = str(limit)
        url = self.base_url + specific_url + "?q=" + query + "&start=" + start + "&limit=" + limit + "&apikey=" + self.api_key
        response_json = self.web_fetch(url)

        #results
        #    *  results[]{} - The sorted list of matched items
        #          o item{} - A matched whitepaper object
        #          o highlight - A short snippet of text highlighting matched keywords
        #    * request{} - The request parameters (from the arguments above)
        #          o q
        #          o start
        #          o limit
        #    * hits - The total number of matched objects
        #    * time - The amount of time it took to process the entire request (in seconds)
        return simplejson.loads(response_json)
    def suggest_part_query(self, query, limit=1):
        '''suggest a part search query string, optimized for speed and useful for auto-complete features
        query: query string with minimum length of 2 characters (required)
        limit: maximum number of results to return (default is 10, max is 10)
        '''
        specific_url = "parts/suggest"

        #some preliminary checks
        if len(query)<2: raise ValueError, "Octopart.suggest_part_query: length of query string must be at least 2 characters"
        if limit>10 or limit<1: raise ValueError, "Octopart.suggest_part_query: limit must be between 1 and 10"
        limit = str(limit)
        
        url = self.base_url + specific_url + "?q=" + query + "&limit=" + limit + "&apikey=" + self.api_key
        response_json = self.web_fetch(url)

        #results
        #    *  results[] - The sorted list of search suggestions
        #    * request{} - The request parameters (from the arguments above)
        #          o q
        #          o limit
        #    * hits - The total number of matched suggestions
        #    * time - The amount of time it took to process the entire request (in seconds)
        return simplejson.loads(response_json)

def octopart_search(query):
    '''searches octopart with the string'''
    octopart = Octopart(octopart_api_key)
    #categories = octopart.get_categories(id=4179)
    #print "categories: %s" % (categories)
    parts = octopart.search_parts(query=query, limit=1)
    #print "parts: %s" % (parts)
    print parts.keys()

class OctopartTests(unittest.TestCase):
    def test_octopart_get_category(self):
        octopart = Octopart(octopart_api_key)
        categories = octopart.get_category(id=4179)
        pass

if __name__ == "__main__":
    optfunc.run(octopart_search)
