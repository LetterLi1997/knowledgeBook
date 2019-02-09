package cellmachine;

import cell.Cell;
import field.Field;
import field.View;

import javax.swing.*;


public class CellMachine {
    private Field field;
    private View view;
    public CellMachine(int size){
        field = new Field(size,size);
        for(int row=0; row<field.getHeight();row++){
            for(int col=0;col<field.getWidth();col++){
                field.place(row,col,new Cell());
            }
        }
        for(int row=0; row<field.getHeight();row++){
            for(int col=0; col<field.getWidth();col++){
                Cell cell = field.get(row,col);
                if(Math.random()<0.2){
                    cell.reborn();
                }
            }
        }
        view = new View(field);
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);
        frame.setTitle("Cells");
        frame.add(view);
        frame.pack();
        frame.setVisible(true);
    }
    public void start(int steps){
        for(int i=0;i<steps;i++){
            step();
            view.repaint();
            try {
                Thread.sleep(200);
            }
            catch (InterruptedException e){
                e.printStackTrace();
            }
        }
    }
    public void step(){
        for(int row = 0;row<field.getHeight();row++) {
            for (int col = 0; col < field.getWidth(); col++) {
                Cell cell = field.get(row, col);
                Cell[] neighbour = field.getNeighbour(row, col);
                int numOfLive = 0;
                for (Cell c : neighbour) {
                    if (c.isAlive()) {
                        numOfLive++;
                    }
                }
                System.out.print("[" + row + "]" + "[" + col + "]:");
                System.out.print(cell.isAlive() ? "live" : "dead");
                System.out.print(":" + numOfLive + "-->");
                if (cell.isAlive()) {
                    if (numOfLive < 2 || numOfLive > 3) {
                        cell.die();
                        System.out.print("die");
                    }
                } else if (numOfLive == 3) {
                    cell.reborn();
                    System.out.print("reborn");
                }
                System.out.println();
            }
        }
    }
    public static void main(String[] args){
        CellMachine cm = new CellMachine(30);
        cm.start(100);
    }
}
