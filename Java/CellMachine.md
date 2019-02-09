# 元胞自动机——自顶向下模式
![]()
首先我们从顶开始构建代码 
## CellMachine.java
1. 创建CellMachine构造函数
2. 创建start()方法
3. 创建step()确定每一步细胞的变化
4. main()方法

### **main()方法**
    
1. 创建一个CellMachine的对象cm并且传入参数为网格的大小30*30
2. 开始游戏并且设置迭代次数100次
```
public static void main(String[] args){
        CellMachine cm = new CellMachine(30);
        cm.start(100);
    }
```
### **创建CellMachine构造函数**
1. 首先双重循环将field每个赋予Cell对象
2. 第二次二重循环 根据概率对每个格子是否初始化产生Cell做判断
3. 调用JFrame，View产生图形化界面
```
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
```
### **创建start()方法**
1.传入一共迭代的次数
```
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
```
### **创建step()确定每一步细胞的变化**
1. 获取当前细胞周围邻居细胞个数
2. 如果细胞不为3个就细胞死亡
3. 如果死细胞周围的细胞数为3个则复活

```
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
```
# 完整效果
![](https://github.com/LetterLi1997/knowledgeBook/blob/master/Java/Images/1.gif?raw=true)

# 完整代码
[详见链接](https://github.com/LetterLi1997/knowledgeBook/tree/master/Java/CellMachine)