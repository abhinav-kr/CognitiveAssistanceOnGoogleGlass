package edu.cmu.cs.gabriel;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.media.AudioManager;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeech.OnInitListener;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;

import com.google.android.glass.media.Sounds;
import com.google.android.glass.widget.CardBuilder;
import com.google.android.glass.widget.CardScrollAdapter;
import com.google.android.glass.widget.CardScrollView;


public class AlgoScrollActivity extends Activity  {

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
                Log.d("abhinav", "Posiiton of click : "+position);
                
                Intent nextIntent = null;
                if(position == 0) {
                	nextIntent = new Intent(AlgoScrollActivity.this, CardScrollActivity.class);
                	nextIntent.putExtra(Const.ALGO_FOR_DETECTION,Const.USING_ESVM);
                } else {
                	nextIntent = new Intent(AlgoScrollActivity.this, GabrielClientActivity.class);
                	nextIntent.putExtra(Const.ALGO_FOR_DETECTION,Const.USING_DPM);
                	nextIntent.putExtra(Const.OBJECT_TO_DETECT, Const.OBJ_ANY);
                }
                

                startActivity(nextIntent);
            }
        });
    }


    private void createCards() {
        mCards = new ArrayList<CardBuilder>();
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.TEXT)
        .setFootnote(" Tap to select.")
        .setText("Use 'Exempler SVM'"));
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.TEXT)
        .setFootnote(" Tap to select.")
        .setText("Use 'DPM'")
        );
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