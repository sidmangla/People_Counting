import darknet
import cv2
import os
from datetime import datetime, timedelta
import traceback
import numpy as np

class SecurityCheck():
	def __init__(self):
		self.FLAG = False
		self.person_dict = {}
		self.del_list=[]
		self.not_checked = []
		self.p_num = 1
		self.diff_pixel = 50
		self.small_diff = 20
		self.exit_count = 0
		self.entry_count = 0
		self.del_item = 0
		self.entry_point = 1520
		self.exit_point = 380
		self.first_phase = [380,760]
		self.second_phase = [760,1140]
		self.third_phase = [1140,1520]
		self.trigger = 'Person'
		self.confidence = 0
		self.model_width = 512
		self.model_height = 512
		self.pr_coord = 0
		self.draw = 0
		self.orientation = "horizontal"
		self.phase_list = ["first","third"]
		#self.guard_x_limit = 50
		#self.guard_y_limit = 50
		self.sec_trig_xlimit = 120
		self.sec_trig_ylimit = 120
		self.checked_count = 0
		self.security_check = 0

	def phase_check(self,ch):
		if ch > self.first_phase[0] and ch < self.first_phase[1]:
			return "first"
		elif ch > self.second_phase[0] and ch < self.second_phase[1]:
			return "second"
		elif ch > self.third_phase[0] and ch < self.third_phase[1]:
			return "third"
		elif ch < self.exit_point:
			return "out"
		elif ch > self.entry_point:
			return "in"

	def Security_entryGate(self,img,result):
		dict_new = {}
		self.del_list=[]
		cord= j[2]
		conf = j[1]
		cl_name = j[0]
		xm=int((cord[0]) * float(x_res/self.model_width)) 
		ym=int((cord[1]) * float(y_res/self.model_height))

		if self.security_check == 1:
			if cl_name == self.sec_trigger and float(conf) > self.sec_confidence and len(self.person_dict) >0:
				for item in self.person_dict:
					if self.person_dict[item]["moving"] == "in" and self.person_dict[item]["prev_phase"] == "second" and self.person_dict[item]["checked"] == 'no':
						if abs(self.person_dict[item]["xco"] - xm) < self.sec_trig_xlimit and abs(self.person_dict[item]["yco"] - ym) < self.sec_trig_ylimit :
							self.person_dict[item]["metal"] = self.person_dict[item]["metal"] + 1
					if self.person_dict[item]["metal"] >= 2 and self.person_dict[item]["checked"] == "no":
						self.checked_count = self.checked_count +1
						self.person_dict[item]["checked"] = "yes"




		if cl_name == self.trigger and float(conf) >= self.confidence:
			if self.pr_coord == 1:
				img = cv2.putText(img, "xm: "+str(xm)+"ym: "+str(ym) , (xm,ym), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 0, 255) , 2, cv2.LINE_AA)
			if self.orientation == "horizontal":
				ch = xm
			else:
				ch = ym
			if len(self.person_dict) == 0:
				self.phase= self.phase_check(ch)
				if self.phase == "first":
					self.person_dict[self.p_num] = {"xco":xm,"yco":ym,"prev_phase":self.phase,"moving":"in","checked":"no"}
				elif self.phase == "third":
					self.person_dict[self.p_num] = {"xco":xm,"yco":ym,"prev_phase":self.phase,"moving":"out"}
					
			elif len(self.person_dict) > 0:
				self.phase = self.phase_check(ch)
				dict_new,dict_same = {}, {}
				for key in self.person_dict:
					if self.orientation == "horizontal":
						old_ch = int(self.person_dict[key]['xco'])
					else:
						old_ch = int(self.person_dict[key]['yco'])
					dist = abs(ch - old_ch)
					print ("Distance from previous frame: "+str(dist))
					if dist < self.diff_pixel:

						if self.phase == "out" and self.person_dict[key]["prev_phase"] == "first" and self.person_dict[key]["moving"] == "out":
							self.exit_count = self.exit_count+1
							self.person_dict[key]["prev_phase"] = "out"
							self.del_list.append(key)

						if self.phase == "second" and self.person_dict[key]["prev_phase"] == "third" and self.person_dict[key]["moving"] == "out":
							self.person_dict[key]["moving"] = "out"
							self.person_dict[key]["prev_phase"] = "second"

						if self.phase == "first" and self.person_dict[key]["prev_phase"] == "second" and self.person_dict[key]["moving"] == "out":
							self.person_dict[key]["moving"] = "out"
							self.person_dict[key]["prev_phase"] = "first"


						if self.phase == "second" and self.person_dict[key]["prev_phase"] == "first" and self.person_dict[key]["moving"] == "in":
							self.person_dict[key]["moving"] = "in"
							self.person_dict[key]["prev_phase"] = "second"

						if self.phase == "third" and self.person_dict[key]["prev_phase"] == "second" and self.person_dict[key]["moving"] == "in":
							self.person_dict[key]["moving"] = "in"
							if self.security_check == 1:
								if self.person_dict[key]["checked"] == "no" and (key not in self.not_checked):
									print("**************************** Security Check not done **************************")
									self.not_checked.append(key)

							self.person_dict[key]["prev_phase"] = "third"

						if self.phase == "in" and self.person_dict[key]["prev_phase"] == "third" and self.person_dict[key]["moving"] == "in":
							self.entry_count = self.entry_count + 1
							self.del_list.append(key)
						
						self.person_dict[key]["xm"] = xm
						self.person_dict[key]["ym"] = ym

					elif  dist > self.diff_pixel and (self.phase in self.phase_list):
						self.p_num = self.p_num +1 
						if self.phase == "first":
							dict_new[self.p_num] = {"xco":xm,"yco":ym,"prev_phase":self.phase,"moving":"in","checked":"no"}
						elif self.phase == "third":
					    	dict_new[self.p_num] = {"xco":xm,"yco":ym,"prev_phase":self.phase,"moving":"out"}
				if len(dict_new) > 0:
					self.person_dict.update(dict_new)
				if len(self.del_list) > 0 and len(self.person_dict) > 1:
					for i in self.del_list:
						self.person_dict.pop(i)



		img = cv2.putText(img, "Entered: "+str(self.entry_count) , (30,150), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 0, 255) , 2, cv2.LINE_AA)
		img = cv2.putText(img, "Exited: :"+str(self.exit_count) , (30,70), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 0, 255) , 2, cv2.LINE_AA)
		if self.security_check == 1:
			img = cv2.putText(img, "Checked: :"+str(self.checked_count) , (30,110), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 0, 255) , 2, cv2.LINE_AA)
			img = cv2.putText(img, "Not Checked: :"+str(len(self.not_checked)) , (30,30), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 0, 255) , 2, cv2.LINE_AA)

		return img

if __name__ == '__main__':
	try:
		font = cv2.FONT_HERSHEY_SIMPLEX
		fourcc = cv2.VideoWriter_fourcc(*"XVID")

		parser = argparse.ArgumentParser()
		parser.add_argument('--config',type='str',required =True)
		args = parser.parser_args()
		file = args.config

		project = SecurityCheck()
		with open(file) as f:
			info = json.load(f)
			#model parameters
			self.weightPath = info['weightPath']
			self.metaPath = info['metaPath']
			self.configPath = info['configPath']

			self.entry_point = info["entry_point"]
			self.exit_point = info["exit_point"]
			self.first_phase = info["first_phase"]
			self.second_phase = info["second_phase"]
			self.third_phase =  info["third_phase"]
			self.trigger = info["trigger"]
			self.confidence = int(info["confidence"])
			self.model_width = int(info["model_width"])
			self.model_height = int(info["model_height"])
			self.draw = int(info["draw"])
			self.pr_coord = int(info["print_coord"])
			self.orientation = info["orientation"]
			
			# security check params
			self.security_check = info["security_check"]
			self.sec_trigger = info["security_trigger"]
			self.sec_confidence = info["security_confidence"]
			self.sec_trig_xlimit = info["sec_trig_xlimit"]
			self.sec_trig_ylimit = info["sec_trig_ylimit"]

			# input could be video file or stream
			cap = cv2.VideoCapture(info["input"])
			fps = info["fps"]
			#network, class_names, class_colors = darknet.load_network(configPath,metaPath,weightPath,batch_size=1)
			#darknet_image = darknet.make_image(darknet.network_width(network),darknet.network_height(network),3)
			self.x_res = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
			self.y_res  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
			loc=info["output"]
			out=cv2.VideoWriter(info["output"], fourcc,fps , (self.x_res,self.y_res), True)
			while cap.isOpened(): 
				ret,img=cap.read()
				if ret is True:
					frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
				else:
					break
				# load model
				#frame_resized = cv2.resize(frame_rgb,(darknet.network_width(network),darknet.network_height(network)),interpolation=cv2.INTER_LINEAR)
				#darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
				#result=darknet.detect_image(network,class_names,darknet_image, thresh=0.25)
				img = SecurityCheck.Security_entryGate(img,result)
				out.write(img)
			cap.release()
			out.release()
			f.close()
	except Exception as e:
		print (str(e))
	cv2.destroyAllWindows()