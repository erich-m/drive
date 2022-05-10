# -*- coding: utf-8 -*-
import mice
import VEN

class Script:
    def __init__(self):        
        self.com = VEN.VENCommunicationSystem()
        # VEN initilization
        self.com.init("224.255.0.1", 64101)
        self.out_sender="DistortionServer"
        self.out_msg="params"
        self.in_sender="DistortionClient"
        self.in_msg=self.out_msg
        
        #focal
        self.focal_length = mice.variables['Focal Length Px']
        #distortion coeff
        self.k1 = mice.variables['k1']
        self.k2 = mice.variables['k2']
        self.p1 = mice.variables['p1']
        self.p2 = mice.variables['p2']
        
        print "Default Values %(focal_length)s, [%(k1)s, %(k2)s, %(p1)s, %(p2)s]" \
                % self.__dict__
        self.update_from_client()        
        
        print "creation ", self
        
    def __del__(self):
        print "destruction " , self
        
    def update_from_client(self):
        param_from_client = []
        if self.com.available(self.in_sender, self.in_msg) \
            and self.com.read_float(self.in_sender, self.in_msg, param_from_client, 5) == 0:
            mice.variables['Focal Length Px'] = param_from_client[0]
            mice.variables['k1'] = param_from_client[1]
            mice.variables['k2'] = param_from_client[2]
            mice.variables['p1'] = param_from_client[3]
            mice.variables['p2'] = param_from_client[4]

            self.focal_length = mice.variables['Focal Length Px']
            self.k1 = mice.variables['k1']
            self.k2 = mice.variables['k2']
            self.p1 = mice.variables['p1']
            self.p2 = mice.variables['p2']
            
            print "New values %(focal_length)s, [%(k1)s, %(k2)s, %(p1)s, %(p2)s]" \
                    % self.__dict__
            
    def send_to_client(self):
        focale = mice.variables['Focal Length Px']
        k1 = mice.variables['k1']
        k2 = mice.variables['k2']
        p1 = mice.variables['p1']
        p2 = mice.variables['p2']
        if focale != self.focal_length or k1 !=self.k1 \
            or k2 != self.k2 or p1 != self.p1 or p2 != self.p2:
            self.com.write_float(self.out_sender, self.out_msg, 
                            [focale, k1, k2, p1, p2])
            #mice.exportChannel(output_focal_lenth_channel, focale)
            self.focal_length = focale
            self.k1 = k1
            self.k2 = k2
            self.p1 = p1
            self.p2 = p2
            print "Send values %(focal_length)s, [%(k1)s, %(k2)s, %(p1)s, %(p2)s]" \
                % self.__dict__

    def main(self):
        self.update_from_client()
        self.send_to_client()
        return self.focal_length