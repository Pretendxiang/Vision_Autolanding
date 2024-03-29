import math
import numpy as np

class AOA:
      def AOA_v0(self, x, y, z, phi, theta, psi, P_img_x, P_img_y, P_img_z):

            ### ENU to NED ###
            theta = -theta

            if 0 < psi:
                  if (np.pi/2) >=psi:
                        psi = np.pi/2-psi
                  else:
                        psi = -(psi-np.pi/2)+2*np.pi
            elif psi < 0:
                  if (-np.pi/2) <=psi:
                        psi = -psi+np.pi/2
                  else:
                        psi = -psi-3*np.pi/2+2*np.pi
            else:
                  psi = psi

            psi = -psi
            ####################

            ##### Coordinate Rotation #####
            ## Camera to Gimbal ##
            ## 1
            #C2G = [[0, 0, 1],[-1, 0, 0],[0, -1, 0]]
            ## 2
            # C2G = [[0, 0, 1],[0, 1, 0],[-1, 0, 0]]

            ## Camera to Body ##
            # roll, pan, tilt = 0, 0, 0
            # C_x = [[1, 0, 0],[0, np.cos(roll), -np.sin(roll)],[0, np.sin(roll), np.cos(roll)]]
            # C_y = [[np.cos(tilt), 0, -np.sin(tilt)], [0, 1, 0], [np.sin(tilt), 0, np.cos(tilt)]]
            # C_z = [[np.cos(pan), -np.sin(pan), 0], [np.sin(pan), np.cos(pan), 0], [0, 0, 1]]
            # C_1 = np.matmul(C_y,C_z)
            # B2G = np.matmul(C_x,C_1)
            # G2B = np.linalg.inv(B2G)

            ## Body to World ##
            R_x = [[1, 0, 0],[0, np.cos(phi), -np.sin(phi)],[0, np.sin(phi), np.cos(phi)]]
            R_y = [[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]]
            R_z = [[np.cos(psi), -np.sin(psi), 0], [np.sin(psi), np.cos(psi), 0], [0, 0, 1]]
            R_1 = np.matmul(R_y,R_z)
            W2B = np.matmul(R_x, R_1)
            B2W = np.linalg.inv(W2B)

            ############ Calculation ###################
            ## Start : from vector in camera coordinate ##
            P_ct = [[P_img_x], [P_img_y], [P_img_z]]
            norm_T = np.linalg.norm(P_ct)
            P_ct_norm = P_ct/norm_T
            L_r = [0, 0, 1]

            # Rotation
            #P_gt = np.matmul(C2G, P_ct_norm)
            # P_bt = np.matmul(G2B, P_gt)
            P_wt = np.matmul(B2W, P_ct_norm)
            # print("P_ct = " , P_ct)
            # print("P_gt = " , P_gt)
            # print("P_bt = " , P_bt)
            # print("P_wt = " , P_wt)
            
            # estimate the scalar
            d = abs(z)/(np.dot(L_r, P_wt))
            # print("z = " , z)
            # print("L_s = " , L_s)
            # print("d = " , d)

            ## Method_1 
            P_world = np.matmul(P_wt, d)
            #print("target position vector = ")
            #print(P_world)

            est_n = P_world[0] + x  
            est_e = P_world[1] + y   
            est_d = P_world[2] + z  
            est = [est_n, est_e, est_d]
            # print("estimation = " , est)

            ## Method_2 unit vector
            vector_n = P_wt[0]
            vector_e = P_wt[1]
            vector_d = P_wt[2]
            est_vector = [vector_n, vector_e, vector_d]
            # print("est_vector = " , est_vector)

            ## a = azimuth angle   ##
            ## e = elevation angle ##
            a_w = np.arctan2(est_e-y, est_n-x)
            a = np.arctan2(vector_e, vector_n)

            e_w = np.arctan2(np.sqrt(np.square(est_n - x) + np.square(est_e - y)), est_d - z)
            e = np.arctan2(np.sqrt(np.square(vector_n) + np.square(vector_e)), vector_d)
            # print('a_w =', a_w)
            # print('a =', a)
            # print('e_w =', e_w)
            # print('e =', e)
      
            return a_w, e_w, a, e, est_n, est_e, est_d, vector_n, vector_e, vector_d

          







