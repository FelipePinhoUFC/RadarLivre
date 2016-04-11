from math_utils.adsb_decoder_library import *
from math_utils.crc_calc import *
from radarlivre_api.models import HalfObservation, Observation

import time

# Aircraft TypeS
cs_tbl = ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', ' ', ' ', ' ', ' ',
          ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', ' ', ' ', ' ', ' ', ' ']

EVEN_PACK = "0"
ODD_PACK = "1"

# Receive an ADS-B message and return a HalfObservation object 
def decodeMessage(adsbMessage):
    data = adsbMessage.data
    
    latHome = adsbMessage.latitude
    lonHome = adsbMessage.longitude

    if len(data) == 28:
        if parity112(data) == False:
            
            # CRC invalido
            return None
        
        # CRC valido
        
        ICAO = data[2:8] #Da pra reduzir
        DFCA = toHex(data[:2]) #Da pra reduzir
        DF = full_bit_zero(bin(eval(DFCA)))[:5] #Da pra reduzir
        DF = eval("0b" + DF) #Da pra reduzir
        CA = full_bit_zero(bin(eval(DFCA)))[5:] #Da pra reduzir
        b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5] #Da pra reduzir
        TC = eval("0b" + b_TC)  #Da pra reduzir
        b_Mode = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[5:] #Tres bits para o mode
      
        if DF == 17:
            # 'Downlink Format: 17 - S Mode'

            if TC >= 1 and TC <= 4:
                # "Type: Airplane Identification Message... (Nome do Voo, Tipo Aeronave)"
                hex_adsb_packet = data[8:] #Da pra reduzir
                bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])
                
                formattypecode = bin_adsb_packet[0] + bin_adsb_packet[1] + bin_adsb_packet[2] + bin_adsb_packet[3] + bin_adsb_packet[4] #Da pra reduzir
                aircrafttype = bin_adsb_packet[5] + bin_adsb_packet[6] + bin_adsb_packet[7] #Da pra reduzir
                char = "" #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[8]+bin_adsb_packet[9]+bin_adsb_packet[10]+bin_adsb_packet[11]+bin_adsb_packet[12]+bin_adsb_packet[13])] #1 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[14]+bin_adsb_packet[15]+bin_adsb_packet[16]+bin_adsb_packet[17]+bin_adsb_packet[18]+bin_adsb_packet[19])] #2 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[20]+bin_adsb_packet[21]+bin_adsb_packet[22]+bin_adsb_packet[23]+bin_adsb_packet[24]+bin_adsb_packet[25])] #3 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[26]+bin_adsb_packet[27]+bin_adsb_packet[28]+bin_adsb_packet[29]+bin_adsb_packet[30]+bin_adsb_packet[31])] #4 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[32]+bin_adsb_packet[33]+bin_adsb_packet[34]+bin_adsb_packet[35]+bin_adsb_packet[36]+bin_adsb_packet[37])] #5 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[38]+bin_adsb_packet[39]+bin_adsb_packet[40]+bin_adsb_packet[41]+bin_adsb_packet[42]+bin_adsb_packet[43])] #6 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[44]+bin_adsb_packet[45]+bin_adsb_packet[46]+bin_adsb_packet[47]+bin_adsb_packet[48]+bin_adsb_packet[49])] #7 #Da pra reduzir
                char = char + cs_tbl[eval("0b"+bin_adsb_packet[50]+bin_adsb_packet[51]+bin_adsb_packet[52]+bin_adsb_packet[53]+bin_adsb_packet[54]+bin_adsb_packet[55])] #8 #Da pra reduzir
                
                obs = HalfObservation()
                obs.airplane = ICAO
                obs.route = char
                obs.latitudeCollector = latHome
                obs.longitudeCollector = lonHome
                obs.timestamp = time.time()
                obs.identityReceived = True
                return obs
       
            elif TC >= 9 and TC <= 18: 
                # "Type: Airborne Position message... (Altitude, Latitude e Longitude) - Altitude Barometrica"
                hex_adsb_packet = data[8:] #Da pra reduzir
                bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])
                Altitude = "0b" + bin_adsb_packet[8:][:12] #Da pra reduzir
                Latitude = eval("0b" + bin_adsb_packet[22:][:17]) #Da pra reduzir   
                Longitude =  eval("0b" + bin_adsb_packet[-17:]) #Da pra reduzir
                T = bin_adsb_packet[20:][0] #Da pra reduzir
                F = bin_adsb_packet[21:][0] #Da pra reduzir

                Altitude = Altitude[2:][:12] #Da pra reduzir
                bits = Altitude[0]+Altitude[1]+Altitude[2]+Altitude[3]+ Altitude[4]+Altitude[5]+Altitude[6]+Altitude[8]+Altitude[9]+Altitude[10]+Altitude[11] #Da pra reduzir
                oitavo_bit = Altitude[7] #Da pra reduzir
                Altitude = 25 * eval("0b"+bits) - 1000 #Da pra reduzir
                # "Altitude: " + str(Altitude)
               
                if F == EVEN_PACK:
                    # Even Packet
                    obs = HalfObservation()
                    obs.airplane = ICAO
                    obs.lastReceived = EVEN_PACK
                    obs.evenReceived = True
                    obs.latitudeEven = Latitude
                    obs.longitudeEven = Longitude
                    obs.altitude = Altitude
                    obs.timestamp = time.time()
                    return obs
                    # UpdateAirplanePosition_T0(ICAO, [Latitude, Longitude, Altitude])
                    
                elif F == ODD_PACK:
                    # Odd Packet
                    
                    obs = HalfObservation()
                    obs.airplane = ICAO
                    obs.lastReceived = ODD_PACK
                    obs.oddReceived = True
                    obs.latitudeOdd = Latitude
                    obs.longitudeOdd = Longitude
                    obs.altitude = Altitude
                    obs.timestamp = time.time()
                    return obs
                    
                    # UpdateAirplanePosition_T1(ICAO, [Latitude, Longitude, Altitude])

                                          
            elif TC == 19:
                # "Type: Airborne Velocity Message... (Ground Speed, Track, Vertical)"
                hex_adsb_packet = data[8:] #Da pra reduzir
                hex_adsb_packet = hex_adsb_packet[:14] #Da pra reduzir
                bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13]) #Da pra reduzir
                subtype = eval("0b"+bin_adsb_packet[5] + bin_adsb_packet[6] + bin_adsb_packet[7]) #Da pra reduzir

                if subtype == 0:
                    pass
                    # "Velocidade: Supersonica... Corre cumpadi"
                
                if subtype == 1: # Velocidade (de Ground) nao supersonica
                    # "Velocidade: Nao-Supersonica"
                    directionBitEastWest = bin_adsb_packet[13]
                    directionBitNorthSouth = bin_adsb_packet[24]

                    numEastWest = eval("0b"+bin_adsb_packet[14]+bin_adsb_packet[15]+bin_adsb_packet[16]+bin_adsb_packet[17]+bin_adsb_packet[18]+bin_adsb_packet[19]+bin_adsb_packet[20]+bin_adsb_packet[21]+bin_adsb_packet[22]+bin_adsb_packet[23]) #Da pra reduzir
                    numNorthSouth = eval("0b"+bin_adsb_packet[25]+bin_adsb_packet[26]+bin_adsb_packet[27]+bin_adsb_packet[28]+bin_adsb_packet[29]+bin_adsb_packet[30]+bin_adsb_packet[31]+bin_adsb_packet[32]+bin_adsb_packet[33]+bin_adsb_packet[34]) #Da pra reduzir

                    gnd_spd = math.floor(math.sqrt(numEastWest * numEastWest + numNorthSouth * numNorthSouth))
            
                    if (numEastWest == 0) and (numNorthSouth == 0):
                        return None
                    else:
                        directionBitEastWest = float(directionBitEastWest)
                        directionBitNorthSouth = float(directionBitNorthSouth)
                        numEastWest = float(numEastWest)
                        numNorthSouth = float(numNorthSouth)

                        trk = 0
                        if directionBitEastWest == 0 and directionBitNorthSouth == 0:
                            if numEastWest == 0:
                                trk = 0
                            else:
                                trk = 90 - 180./math.pi*math.atan(numNorthSouth / numEastWest)
                        
                        if directionBitEastWest == 0 and directionBitNorthSouth == 1:
                            if numEastWest == 0:
                                trk = 180
                            else:
                                trk = 90 + 180./math.pi*math.atan(numNorthSouth / numEastWest)

                        if directionBitEastWest == 1 and directionBitNorthSouth == 1:
                            if numEastWest == 0:
                                trk = 180
                            else:
                                trk = 270 - 180./math.pi*math.atan(numNorthSouth / numEastWest)

                        if directionBitEastWest == 1 and directionBitNorthSouth== 0:
                            if numEastWest == 0:
                                trk = 0
                            else:
                                trk = 270 + 180./math.pi*math.atan(numNorthSouth / numEastWest)
                            
                        if (trk - int(math.floor(trk))) < 0.5:
                            trk = int(math.floor(trk))
                        else:
                            trk = int(math.ceil(trk))
                                    
                        obs = HalfObservation()
                        obs.airplane = ICAO
                        obs.velocityReceived = True
                        obs.angle = trk
                        obs.horizontalVelocity = gnd_spd
                        obs.verticalVelocity = 0
                        obs.timestamp = time.time()
                        return obs
                
            else:
                return None
                # 'Downlink Format: ' +str(DF) + ' Type Code:'+ str(TC) +' - Desconhecido'
                # ServerReport.report('PyAdsbDecoderDataBase', '1', 'Downlink Format/type code: ' +str(DF)+"/" + str(TC) + ' - Desconhecido - '+ data)

    else:
        return None
        # 'Tamanho de invalido do pacote...'
        # ServerReport.report('PyAdsbDecoderDataBase', '1', 'Tamanho de invalido do pacote - '+ data)

def fromHalfObservation(halfObservation):
    Airplanes1 = int(halfObservation.latitudeEven)
    Airplanes2 = int(halfObservation.latitudeOdd)
    Airplanes3 = int(halfObservation.longitudeEven)
    Airplanes4 = int(halfObservation.longitudeOdd)
    j = math.floor((59. * Airplanes1 - 60. * Airplanes2) / 131072. + 0.5)
    rlat0 = 6. * (modulo(j, 60.) + Airplanes1 / 131072.)
    rlat1 = 6.101694915254237288 * (modulo(j, 59.) + Airplanes2 / 131072.)
   
    if rlat0 > 270:
        rlat0 = rlat0 - 360
    if rlat1 > 270:
        rlat1 = rlat1 - 360

    NL0 = NL(rlat0)
    NL1 = NL(rlat1)
                                           
    if NL0 != NL1:
        # print "Returning null 0" 
        return None

    m = math.floor((Airplanes3 * (NL0 - 1) - Airplanes4 * NL1) / 131072. + 0.5);

    if halfObservation.lastReceived == EVEN_PACK:
        Latitude = rlat0
       
        if NL0 > 1:
            ni = NL0
        else:
            ni = 1
       
        dlon = 360. / ni
        rlon = dlon * (modulo(m, ni) + Airplanes3 / 131072.)
        Longitude = rlon

        if distance(Latitude, Longitude, float(halfObservation.latitudeCollector), float(halfObservation.longitudeCollector)) > 440:
            # print "Pacote Rejeitado - Distancia Muito longa.[", halfObservation.latitudeCollector, halfObservation.longitudeCollector, "] : [", Latitude, Longitude, "]" 
            # print "Returning null 1"
            return None

        now = time.time() * 1000

        obs = Observation()
        # obs.airplane = halfObservation.airplane
        # obs.route = halfObservation.route
        obs.latitude = Latitude
        obs.longitude = Longitude
        obs.altitude = halfObservation.altitude
        obs.verticalVelocity = halfObservation.verticalVelocity
        obs.horizontalVelocity = halfObservation.horizontalVelocity
        obs.angle = halfObservation.angle
        obs.timestamp = now - (halfObservation.timestampSent - halfObservation.timestamp)
        
        return obs
       
    elif halfObservation.lastReceived == ODD_PACK:
        Latitude = rlat1
       
        if (NL1 - 1) > 1:
            ni = (NL1 - 1)
        else:
            ni = 1
       
        dlon = 360. / ni
        rlon = dlon * (modulo(m, ni) + Airplanes4 / 131072.)
        Longitude = rlon

        if distance(Latitude, Longitude, float(halfObservation.latitudeCollector), float(halfObservation.longitudeCollector)) > 440:
            # print "Pacote Rejeitado - Distancia Muito longa.[", halfObservation.latitudeCollector, halfObservation.longitudeCollector, "] : [", Latitude, Longitude, "]"
            # print "Returning null 2"
            return None

        now = time.time() * 1000

        obs = Observation()
        # obs.airplane = halfObservation.airplane
        # obs.route = halfObservation.route
        obs.latitude = Latitude
        obs.longitude = Longitude
        obs.altitude = halfObservation.altitude
        obs.verticalVelocity = halfObservation.verticalVelocity
        obs.horizontalVelocity = halfObservation.horizontalVelocity
        obs.angle = halfObservation.angle
        obs.timestamp = now - (halfObservation.timestampSent - halfObservation.timestamp)
        
        return obs
    
    # print halfObservation.lastReceived
    