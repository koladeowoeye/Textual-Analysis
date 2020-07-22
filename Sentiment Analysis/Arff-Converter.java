/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jsentiment;

/**
 *
 * @author wande
 */
import java.io.*;
import java.util.Scanner;
public class Jsentiment {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       
     try
		{
		PrintWriter p = new PrintWriter(new File("2ndnigeria.arff"));
		p.append("@RELATION SentimentDataset\n\n");
                p.append("@ATTRIBUTE affairs	INTEGER\n");
                p.append("@ATTRIBUTE cnn    INTEGER\n");
                p.append("@ATTRIBUTE court    INTEGER\n");
		p.append("@ATTRIBUTE crime INTEGER\n");
		p.append("@ATTRIBUTE ebola INTEGER\n");
		p.append("@ATTRIBUTE facebook	INTEGER\n");
		p.append("@ATTRIBUTE family	INTEGER\n");
                p.append("@ATTRIBUTE government	INTEGER\n");
                p.append("@ATTRIBUTE islam INTEGER\n");
                p.append("@ATTRIBUTE jihad	INTEGER\n");
                p.append("@ATTRIBUTE military    INTEGER\n");
                p.append("@ATTRIBUTE muslims  INTEGER\n");
		p.append("@ATTRIBUTE news INTEGER\n");
		p.append("@ATTRIBUTE policy INTEGER\n");
		p.append("@ATTRIBUTE politics	INTEGER\n");
		p.append("@ATTRIBUTE president	INTEGER\n");
                p.append("@ATTRIBUTE press	INTEGER\n");
                p.append("@ATTRIBUTE program	INTEGER\n");
                p.append("@ATTRIBUTE right INTEGER\n");
                p.append("@ATTRIBUTE safeguards	INTEGER\n");
                p.append("@ATTRIBUTE security    INTEGER\n");
                p.append("@ATTRIBUTE syria  INTEGER\n");
		p.append("@ATTRIBUTE trial INTEGER\n");
		p.append("@ATTRIBUTE twitter INTEGER\n");
		p.append("@ATTRIBUTE victims	INTEGER\n");
		p.append("@ATTRIBUTE war	INTEGER\n");
		p.append("@ATTRIBUTE CLASS	{pro_extremist,anti_extremist,neutra}\n");
		p.append("@DATA\n");	
		//Scanner sc = new Scanner(System.in);
		int[][] datas = new int[179][26];
for(int b=0;b<datas.length;b++)for(int g=0;g<datas[b].length;g++)datas[b][g]=-999;
		for(int k = 0;k<26;k++){
			//String fn = sc.next();
			Scanner s = new Scanner(new File((k+1) + ".txt"));
			int count=0,  ppn=0;
			double sum=0;
			int pgnum;
			while(s.hasNextLine())
			{
				String xx = s.nextLine();
				Scanner xo = new Scanner(xx);
				//System.out.println(xx);
				String[] bb = xx.split(" ");
				if(bb.length>3)
				{
					//System.out.println(bb[2]);					
					int score = Integer.parseInt(xo.next()) + Integer.parseInt(xo.next());
					String vc = xo.next();
					if(vc.substring(8,9).equals("."))
						pgnum = Integer.parseInt(vc.substring(7,8));
					else if(vc.substring(9,10).equals("."))
						pgnum = Integer.parseInt(vc.substring(7,9));
					else if(vc.substring(10,11).equals("."))
						pgnum = Integer.parseInt(vc.substring(7,10));
					else
						pgnum = Integer.parseInt(vc.substring(7,11));
					
					datas[pgnum-1][k] = score;
					
					if(pgnum==ppn){
						sum += score;
						count++;
						ppn=pgnum;
					}
					else{
						if(count>1){datas[ppn-1][k]=(int)Math.ceil(sum/count);}
						
						sum = score;
						ppn=pgnum;
						count=1;
					}
					
				}
			}
		}
		
		for(int a=0; a<datas.length;a++){
			for(int b=0;b<datas[a].length;b++)
			{
				//if(datas[a][b]=0)
				p.append(datas[a][b] + ",");
			}
			if(a<57)p.append("positive");
			else if(a<119)p.append("neutral");
			else p.append("negative");
			p.append("\n");
		}
		p.close();	
		}
		catch(FileNotFoundException e)
		{
			
		}
	}
}
