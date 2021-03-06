import os
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class DeepQNetwork(nn.Module):
    def __init__(self, lr, n_actions, name, input_dims, chkpt_dir, fc1_dims=64, fc2_dims=64, p=0.0, weight_decay=1e-6):
        super(DeepQNetwork, self).__init__()
        self.checkpoint_dir = chkpt_dir
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name)

#        self.conv1 = nn.Conv2d(input_dims[0], 32, 8, stride=4)
#        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
#        self.conv3 = nn.Conv2d(64, 64, 3, stride=1)

#        fc_input_dims = self.calculate_conv_output_dims(input_dims)

        self.fc1 = nn.Linear(*input_dims, fc1_dims)
        self.fc2 = nn.Linear(fc1_dims, fc2_dims)
        self.fc3 = nn.Linear(fc2_dims, n_actions)
        self.dropout = nn.Dropout(p) 

#        self.optimizer = optim.RMSprop(self.parameters(), lr=lr)
        self.optimizer = optim.Adam(self.parameters(), lr=lr, weight_decay=weight_decay)

#        self.loss = nn.MSELoss()
        self.loss = nn.SmoothL1Loss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
#        actions = F.relu(self.fc1(state))
#        actions = F.relu(self.fc2(actions))
#        actions = self.dropout(actions) # dropout for regularization
#        actions = self.fc3(actions)

        actions = T.tanh(self.fc1(state))
        actions = T.tanh(self.fc2(actions))
        actions = self.dropout(actions) # dropout for regularization
        actions = self.fc3(actions)

        
        return actions

    def save_checkpoint(self):
        print('... saving checkpoint ...')
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self, ):
        print('... loading checkpoint ...')
        if self.device.type == 'cpu':
            self.load_state_dict(T.load(self.checkpoint_file,map_location=T.device('cpu')))
        else:            
            self.load_state_dict(T.load(self.checkpoint_file))
