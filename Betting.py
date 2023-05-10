import numpy as np

""""" 
Author : Amine Rguig

"""""

class Betting:
    """""
    Class for Betting Stategies : Strategies Implemented (Level Stakes Betting ), (KellyBetting with increasing stakes),
    (Kelly Betting with unit stakes ), To be implemented : Risk minimization, Optimisation over multiples Stackes
    """""
    def __init__(self, stack=1):

        self.stack_kelly = stack            #### Stack for kelly Betting
        self.stack_unitbet=100              #### Stack for level stakes unit betting
        self.stack_kelly_unit=0             #### Stack for kelly unit
        self.number_of_bets=0               #### number of bets in kelly unit bettings

    def kelly_criterion(self, win_prob, odds):
        """
        Kelly betting criterion 
        
        win_prob: probability
        odds: Bookie odds
        """
        kelly_f = (odds*win_prob-1.)/(odds-1.)
        return max(kelly_f,0)
    
    def kelly_betting(self,proba,y,Over_cote,Under_cote):
        """
        Normal Kelly Betting


        Proba : List of Forecast Probabilities
        y : List of results of games
        Over_cote : Bookie Cote for Over2.5 
        Under_cote : Bookie Cote for Under2.5
        
        """
        
            
        n=len(y)
        s=0
        L=[]
        Profit=0
        Loss=0

        for i in range(n):
            ###Choose betting over or under
            maxk=np.max(proba[i])
            k=np.where(proba[i]==maxk)[0][0]
                     
            ###Choose betting over or under
            if k ==1:
                f=self.kelly_criterion(proba[i][k],Over_cote[i])
            else:
                f=self.kelly_criterion(proba[i][k],Under_cote[i])
            
            s+=f            ### summing proportion
                    
            if s > 1 :          ####Making sure proportion dont go over 1 
                break

            L.append([k,f]) ###appending the decisions of betting 
             
        n0=len(L)           #### Number of eligibe bets
        
        if s == 0 :
            print('no betting')
        else:
            for i in range(n0):
                
                if y[i] == L[i][0] :        ## Winning
                    if y[i] == 1 :
                        Profit+=L[i][1]*Over_cote[i]
                    else :
                        Profit+=L[i][1]*Under_cote[i]
                else:                    #### Losing
                    Loss+=L[i][1]

        self.stack_kelly=(Profit-Loss)*self.stack_kelly+(1-s)*self.stack_kelly    ### (gain-ou perte de l'argent investi) + (reste de l'argent non investi)

        return Profit-Loss
       
    def accuracy(self,y,proba):
        """" 
        Accuracy of forecasts 
        
        """""

        s=0
        for i in range(len(y)):
            maxk=np.max(proba[i])
            k=np.where(proba[i]==maxk)[0][0]
            if k == y[i]:
                s+=1
        return s

    def level_stakes_betting(self,win_prob,prob_odds):
        if win_prob > prob_odds:
           
            return 1
        return 0
    def kellybetting_unit(self,prob,y,over,under,treshold):
        """""
        Unit betting kelly (Bosckanov 2017)
        Not accumulative betting, betting of proportion only


        prob : list 2x1 [prob of Under 2.5,prob of Over 2.5]
        y: Result 1 if Over 2.5 0 if not
        treshold: Value Betting treshold 
        """""
        prob_under=prob[0]
        prob_over=prob[1]
        f_over=self.kelly_criterion(prob_over,over)
        f_under=self.kelly_criterion(prob_under,under)
        
        criter_over=f_over*(over-1)
        criter_under=f_under*(under-1)
        
        if max(criter_over,criter_under) > treshold : 
            self.stack_kelly_unit+=1
            self.number_of_bets+=1
            if criter_over > criter_under :
                if y == 1:  
                    self.stack_kelly_unit+=criter_over
                else:
                    self.stack_kelly_unit+= (-f_over)
            else:
                if y ==0:
                    self.stack_kelly_unit+=criter_under
                else:
                    self.stack_kelly_unit+= (-f_under)
        
        return self.stack_kelly_unit
    def kellybetting_unitlist(self,prob,y,over,under,treshold):
        """""
        Same Function as above but for multiple bets

        """""
        n=len(y)
        L=[]
        for i in range(n):
            b=self.kellybetting_unit(prob[i],y[i],over[i],under[i],treshold)
            L.append(b)
        return L
            
    