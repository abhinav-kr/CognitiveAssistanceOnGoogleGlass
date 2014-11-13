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


public class CardScrollActivity extends Activity implements TextToSpeech.OnInitListener {

    private List<CardBuilder> mCards;
    private CardScrollView mCardScrollView;
    private ExampleCardScrollAdapter mAdapter;
    TextToSpeech mTTS = null;

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
		mTTS = new TextToSpeech(this, this);
    }
    
    private void setupClickListener() {
        mCardScrollView.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                mTTS.speak("Starting stream", TextToSpeech.QUEUE_FLUSH, null);
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
                mTTS.shutdown();
                startActivity(gabrielIntent);
            }
        });
    }


    private void createCards() {
        mCards = new ArrayList<CardBuilder>();
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.COLUMNS)
        .setText("Looking for 'Cup'")
        .addImage(R.drawable.cup));
        
        mCards.add(new CardBuilder(this, CardBuilder.Layout.COLUMNS)
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

	@Override
	public void onInit(int status) {
		if (status == TextToSpeech.SUCCESS) {
			if (mTTS == null){
				mTTS = new TextToSpeech(this, this);
			}
			int result = mTTS.setLanguage(Locale.US);
			if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
				Log.e("krha_app", "Language is not available.");
			}
		} else {
			// Initialization failed.
			Log.e("krha_app", "Could not initialize TextToSpeech.");
		}
	}
}