import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseArray

class Leanstep(Node):
    def __init__(self):
        super().__init__('steplearner')
        self.joint_states=None
        self.subscription = self.create_subscription(
            JointState,f'joint_states',self.currentpose,1)
        self.posesub = self.create_subscription(
            PoseArray,f'pose',self.getpose,1)
        self.jointscontroller={}
        for legparts in range(3):
            for legidx in range(3):
                ltpname=f'l{legidx+1}leg{legparts+1}j'
                rtpname=f'r{legidx+1}leg{legparts+1}j'
                ltmppub= self.create_publisher(Float64, ltpname, 1)
                rtmppub= self.create_publisher(Float64, rtpname, 1)
                self.jointscontroller[ltpname]=ltmppub
                self.jointscontroller[rtpname]=rtmppub   
        #self.get_logger().info(self.jointscontroller)
        self.states=self.getstates()
        self.curstate='unknow'
        self.timer = self.create_timer(1, self.timer_callback)  # 将定时器周期设为0  
          
    def currentpose(self,joint_states):
        self.joint_states=joint_states
        #print(joint_states.name,joint_states.position)
        #self.get_logger().info(''.join(self.joint_states.name))
        #self.get_logger().info(self.joint_states.position)
        
    def getpose(self,pose):
        bodypose=pose.poses[0]
        #print(bodypose)
    def timer_callback(self):
        
        if self.curstate=='unknow':
            st=self.states['stand']
            self.curstate='stand'
        elif self.curstate=='stand':
            st=self.states['leftlift']
            self.curstate='leftlift'
        elif self.curstate=='leftlift':
            st=self.states['leftgo']
            self.curstate='leftgo'
        elif self.curstate=='leftgo':
            st=self.states['leftdown']
            self.curstate='leftdown'
        elif self.curstate=='leftdown':
            st=self.states['rightlift']
            self.curstate='rightlift'
        elif self.curstate=='rightlift':
            st=self.states['leftback']
            self.curstate='leftback'
        elif self.curstate=='leftback':
            st=self.states['rightgo']
            self.curstate='rightgo'
        elif self.curstate=='rightgo':
            st=self.states['rightdown']
            self.curstate='rightdown'
        elif self.curstate=='rightdown':
            #st=self.states['rightback']
            #self.curstate='rightback'
            st=self.states['leftlift']
            self.curstate='leftlift'
        else:
            self.curstate='unknow'
            st=self.states['stand']
            
        print(self.curstate)
        self.run(st)
        
    def run(self,state):
        for joint in state:
            self.jointscontroller[joint].publish(Float64(data=float(state[joint])))
    def getstates(self):
        statesnames='stand', 'leftlift', 'leftgo','leftdown', 'rightlift', 'leftback','rightgo','rightdown','rightback'
        states=[]
        stand={'l1leg1j':0.0, 
               'l2leg1j':0.0,
               'l3leg1j':0.0, 
               'r1leg1j':0.0,
                'r2leg1j':0.0,
                'r3leg1j':0.0,
                'l1leg2j':-0.57,
                'l2leg2j':-0.57, 
                'l3leg2j':-0.57, 
                'r1leg2j':0.57, 
                'r2leg2j':0.57, 
                'r3leg2j':0.57, 
                'l1leg3j':-1.0, 
                'l2leg3j':-1.0, 
                'l3leg3j':-1.0, 
                'r1leg3j':1.0, 
                'r2leg3j':1.0, 
                'r3leg3j':1.0, 
        }
        states.append(stand)

        tmpd=self.liftup('left')
        tmp=stand.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.go('left')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.liftdown('left')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.liftup('right')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.back()
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.go('right')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.liftdown('right')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)

        tmpd=self.back('right')
        tmp=tmp.copy()
        tmp.update(tmpd)
        states.append(tmp)
        return dict(zip(statesnames,states))

        

    def stand(self):
        for i in range(3):
            lname=f'l{i+1}leg2j'
            rname=f'r{i+1}leg2j'
            self.jointscontroller[lname].publish(Float64(data=-0.57))
            self.jointscontroller[rname].publish(Float64(data=0.57))
        for i in range(3):
            lname=f'l{i+1}leg3j'
            rname=f'r{i+1}leg3j'
            self.jointscontroller[lname].publish(Float64(data=-1.0))
            self.jointscontroller[rname].publish(Float64(data=1.0))
    def liftup(self,side='left'):
        if side=='left':
            legs=['l2','r1','r3']
        else:
            legs=['l1','l3','r2']
        states={}
        for leg in legs:
            states[leg+'leg2j']=0.0
        return states
    
    def liftdown(self,side='left'):
        if side=='left':
            legs=['l2','r1','r3']
        else:
            legs=['l1','l3','r2']
        states={}
        for leg in legs:
            if 'l' in leg:
                states[leg+'leg2j']=-0.57
            else:
                states[leg+'leg2j']=0.57
        return states
        
    def go(self,side='left'):
        if side=='left':
            legs=['l2','r1','r3']
        else:
            legs=['l1','l3','r2']
        states={}
        for leg in legs:
            if 'l' in leg:
                states[leg+'leg1j']=-0.2
            else:
                states[leg+'leg1j']=0.2
        return states
        
    def back(self,side='left'):
        if side=='left':
            legs=['l2','r1','r3']
        else:
            legs=['l1','l3','r2']
        states={}
        for leg in legs:
            if 'l' in leg:
                states[leg+'leg1j']=0.2
            else:
                states[leg+'leg1j']=-0.2
        return states



    def goforward(self):
        pass

def main():
    rclpy.init(args=None)

    learnstep = Leanstep()

    rclpy.spin(learnstep)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    learnstep.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
