# ListView 最常用和最难用的控件
在学习安卓界面布局的时候，ListView算是第一个涉及到比较多知识的示例。

1. 接口List和实现ArrayList
2. 适配器实现类——ArrayAdapter并传入泛型
3. 使用convertView喝ViewHolder提高运行效率
4. 通过Toast提示鼠标点击事件


## 主程序
- 通过成员变量定义了水果数组
- 使用了ArrayAdapter适配器
```
package com.example.letterli.application;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import java.util.ArrayList;
import java.util.List;

public class Application extends AppCompatActivity {
    private String[] data = {
            "Apple","Banana","Orange","Watermelon","Pear","Grape","Pineapple","strawberry","Cherry","Mango","Apple","Banana","Orange","Watermelon","Pear","Grape","Pineapple","strawberry","Cherry","Mango"
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_application);

// Application.this 为上下文
// simple_expandable_list_item_1 为安卓自带为listview定义的布局格式
// 实例化这个适配器对象 adapter 相当于把（String）数据和布局一一对应绑定起来
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(Application.this, android.R.layout.simple_expandable_list_item_1, data);
// 找到布局文件
        ListView listView = (ListView) findViewById(R.id.list_view);
// 通过适配器将数据在布局中显示出来
        listView.setAdapter(adapter);
    }
}
```
可以看到这是比较简单的实现方式，我们尝试用List形式来显示Fruit对象（实现同时显示水果与水果的图片）
## 主程序new
```
package com.example.letterli.application;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import java.util.ArrayList;
import java.util.List;

public class Application extends AppCompatActivity {
    private List<Fruit> fruitList = new ListArray<Fruit>();

    /* 重新定义的主程序
    * initFruit(): 初始化水果列表
    * Fruit: 定义了水果的类
    * FruitAdapter: 继承了 ArrayAdapter<Fruit>
    *     
    */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_application);

        initFruit();
// Application.this 为上下文
// simple_expandable_list_item_1 为安卓自带为listview定义的布局格式
// 定义了专门的水果适配器类 adapter 相当于把数据和布局一一对应绑定起来
        FruitAdapter adapter = new FruitAdapter(Application.this, R.layout.fruit_item, fruitList);
// 找到布局文件
        ListView listView = (ListView) findViewById(R.id.list_view);
// 通过适配器将数据在布局中显示出来
        listView.setAdapter(adapter);
    }

    public void initFruit(){
        Fruit apple = new Fruit("apple",apple_pic)
        fruitList.add(apple)
        Fruit banana = new Fruit("banana",banana_pic)
        fruitList.add(banana)
        Fruit orange = new Fruit("orange",orange_pic)
        fruitList.add(orange)
        Fruit watermelon = new Fruit("watermelon",watermelon_pic)
        fruitList.add(watermelon)
        Fruit pear = new Fruit("pear",pear_pic)
        fruitList.add(pear)
        Fruit grape = new Fruit("grape",grape_pic)
        fruitList.add(grape)
        Fruit pineapple = new Fruit("pineapple",pineapple_pic)
        fruitList.add(pineapple)
    }
}
```
## 创建Fruit类
```
package com.example.letterli.application;

public class Fruit {
    private String name;
    private int imageId;

    public Fruit(String name, int imageId){
        this.name = name;
        this.imageId = imageId;
    }

    public String getName(){
        return name;
    }
    public int getImageId(){
        return imageId;
    }
}
```

## 定义水果适配器FruitAdapter
```
package com.example.letterli.application;

public class FruitAdapter extends ArrayAdapter<Fruit> {
    
    /* getView 通过getItem()方法得到当前项的Fruit实例
    * getItem(position): 获取当前的Fruit实例
    * inflate: 获取当前布局资源ID,并且将它填充到上下文中getContext()
    * */
    private int ResourceId;
    FruitAdapter(Context context, int textViewResourceId, List<Fruit> objects) {
        super(context, textViewResourceId, objects);
        resourceId = textViewResourceId;
    }

    @override
    public View getView(int position, View convertView, ViewGroup parent) {
        /* getView 通过getItem()方法得到当前项的Fruit实例
        * getItem(position): 获取当前的Fruit实例
        * inflate: 获取当前布局资源ID,并且将它填充到上下文中getContext()
        * */
        Fruit fruit = getItem(position);
        View view = LayoutInflater.from(getContext()).inflate(resourceId, parent, false);
        ImageView fruitImage = (ImageView) view.findViewById(R.id.fruit_image);
        TextView fruitName = (TextView) view.findViewById(R.id.fruit_name);
        fruitImage.setImageResource(fruit.getImageId());
        fruitName.setText(fruit.getName());
        return view;
    }
}
```