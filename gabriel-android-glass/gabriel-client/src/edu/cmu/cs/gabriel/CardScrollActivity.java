package edu.cmu.cs.gabriel;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;

import com.google.android.glass.widget.CardBuilder;
import com.google.android.glass.widget.CardScrollAdapter;
import com.google.android.glass.widget.CardScrollView;


public class CardScrollActivity extends Activity {

    private List<CardBuilder> mCards;
    private CardScrollView mCardScrollView;
    private ExampleCardScrollAdapter mAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        createCards();
        
        mCardScrollView = new CardScrollView(this);
        mAdapter = new ExampleCardScrollAdapter();
        mCardScrollView.setAdapter(mAdapter);
        
        mCardScrollView.activate();
        
        setupClickListener();
        setContentView(mCardScrollView);
    }
    
    private void setupClickListener() {
        mCardScrollView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                
                Intent gabrielIntent = new Intent(CardScrollActivity.this, GabrielClientActivity.class);                
                String obj = Const.OBJ_CUP;
                if ( position == 0 ) {
                	obj = Const.OBJ_CUP;
                } else if ( position ==1 ) {
                	obj = Const.OBJ_WALLET;
                }
                
                //Intent currIntent = getIntent();
                //Log.d("abhinav","Current algorithm : "+ currIntent.getStringExtra(Const.ALGO_FOR_DETECTION));
                
                gabrielIntent.putExtra(Const.ALGO_FOR_DETECTION, Const.USING_ESVM);
                gabrielIntent.putExtra(Const.OBJECT_TO_DETECT, obj);
                startActivity(gabrielIntent);
            }
        });
    }


    private void createCards() {
        mCards = new ArrayList<CardBuilder>();
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.COLUMNS)
        .setFootnote(" Tap to continue.")
        .setText("Looking for 'Cup'")
        .addImage(R.drawable.cup));
        
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.COLUMNS)
        .setFootnote(" Tap to continue.")
        .setText("Looking for 'Wallet'")
        .addImage(R.drawable.wallet));
    }
    
    private class ExampleCardScrollAdapter extends CardScrollAdapter {
        @Override
        public int getPosition(Object item) {
            return mCards.indexOf(item);
        }

        @Override
        public int getCount() {
            return mCards.size();
        }

        @Override
        public Object getItem(int position) {
            return mCards.get(position);
        }

        @Override
        public int getViewTypeCount() {
            return CardBuilder.getViewTypeCount();
        }

        @Override
        public int getItemViewType(int position){
            return mCards.get(position).getItemViewType();
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            return mCards.get(position).getView(convertView, parent);
        }

    }


}