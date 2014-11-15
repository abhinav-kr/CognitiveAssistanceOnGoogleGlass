package edu.cmu.cs.gabriel;

import java.io.IOException;
import java.util.List;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ImageFormat;
import android.graphics.Paint;
import android.graphics.PorterDuff.Mode;
import android.hardware.Camera;
import android.hardware.Camera.PreviewCallback;
import android.hardware.Camera.Size;
import android.util.AttributeSet;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class CameraPreview extends SurfaceView implements SurfaceHolder.Callback {
	/*
	 * Galaxy Nexus
	 * 320x240	: 2 Mbps, 24 FPS
	 * 640x480	: 3 Mbps, 10 FPS
	 * 800x480	: 2.5Mbps, 7.5 FPS 
	 */

	public SurfaceHolder mHolder;
	public Camera mCamera = null;
	public List<int[]> supportingFPS = null;
	public List<Camera.Size> supportingSize = null;
	
	
	private Paint paint = new Paint();
	private int x1=0, y1=0, x2=0, y2=0;

	public void close() {
		if (mCamera != null) {
			mCamera.stopPreview();
			mCamera.release();
			mCamera = null;
		}
	}

	public CameraPreview(Context context, AttributeSet attrs) {
		super(context, attrs);
		Log.d("krha_debug", "context : " + context);
		if (mCamera == null) {

			// Launching Camera App using voice command need to wait.  
			// See more at https://code.google.com/p/google-glass-api/issues/list
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {}
			mCamera = Camera.open();
		}

		mHolder = getHolder();
		mHolder.addCallback(this);
		mHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
	}

	@Override
	protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
		// TODO Auto-generated method stub
		super.onMeasure(widthMeasureSpec, heightMeasureSpec);
	}

	public void changeConfiguration(int[] range, Size imageSize) {
		Camera.Parameters parameters = mCamera.getParameters();
		if (range != null){
			Log.d("krha", "frame rate configuration : " + range[0] + "," + range[1]);
			parameters.setPreviewFpsRange(range[0], range[1]);			
		}
		if (imageSize != null){
			Log.d("krha", "image size configuration : " + imageSize.width + "," + imageSize.height);
			parameters.setPreviewSize(imageSize.width, imageSize.height);
			parameters.setPictureFormat(ImageFormat.JPEG);			
		}
		
		mCamera.setParameters(parameters);
	}

	public void surfaceCreated(SurfaceHolder holder) {

		if (mCamera == null) {
			mCamera = Camera.open();
			// mCamera.setDisplayOrientation(90);
		}
		if (mCamera != null) {
			try {
				setWillNotDraw(false); 
				mCamera.setPreviewDisplay(holder);
				// set fps to capture
				Camera.Parameters parameters = mCamera.getParameters();
				List<int[]> supportedFps = parameters.getSupportedPreviewFpsRange();
				if(this.supportingFPS == null)
					this.supportingFPS = supportedFps;
				int index = 0, fpsDiff = Integer.MAX_VALUE;
				for (int i = 0; i < supportedFps.size(); i++){
					int[] frameRate = supportedFps.get(i);
					int diff = Math.abs(Const.MIN_FPS*1000 - frameRate[0]);
					if (diff < fpsDiff){
						fpsDiff = diff;
						index = i;
					}
				}
				int[] targetRange = supportedFps.get(index);
				
				// set resolusion
				List<Camera.Size> supportedSizes = parameters.getSupportedPreviewSizes();
				if(this.supportingSize == null)
					this.supportingSize = supportedSizes;
				index = 0;
				int sizeDiff = Integer.MAX_VALUE;
				for (int i = 0; i < supportedSizes.size(); i++){
					Camera.Size size = supportedSizes.get(i);
					int diff = Math.abs(size.width - Const.IMAGE_WIDTH);
					if (diff < sizeDiff){
						sizeDiff = diff;
						index = i;
					}
				}
				Camera.Size target_size = supportedSizes.get(index);
				List<Integer> supportedFormat = parameters.getSupportedPreviewFormats();
				
				changeConfiguration(targetRange, target_size);
				mCamera.startPreview();

			} catch (IOException exception) {
				Log.e("Error", "exception:surfaceCreated Camera Open ");
				this.close();
			}
		}
	}

	public void surfaceDestroyed(SurfaceHolder holder) {
		this.close();
	}

	public void surfaceChanged(SurfaceHolder holder, int format, int w, int h) {
		/*
		 * Camera.Parameters parameters = mCamera.getParameters();
		 * parameters.setPreviewSize(w, h); mCamera.setParameters(parameters);
		 * mCamera.startPreview();
		 */
	}

	public void setPreviewCallback(PreviewCallback previewCallback) {
		if (this.mCamera != null){
			mCamera.setPreviewCallback(previewCallback);
		}
	}

	public Camera getCamera() {
		return mCamera;
	}
	
	/*
	 * To set the rectangle, pass positive integer values
	 * To remove the rectangle, set all the parameters as zeroes.
	 */
	public void setRectangle(int x1, int y1, int x2, int y2) {
		this.x1 =x1;
		this.y1 =y1;
		this.x2 =x2;
		this.y2 = y2;
		this.invalidate();
	}
	
	@Override
	protected void onDraw(Canvas canvas) {
		this.paint.setStrokeWidth(5);        
		this.paint.setStyle(Paint.Style.STROKE); 
		this.paint.setColor(Color.RED);
		
		if(this.x1==0 && this.y1==0 && this.x2==0 && this.y2==0) {
			canvas.drawColor(0, Mode.CLEAR);
		} else {
			canvas.drawRect(this.x1, this.y1, this.x2, this.y2, paint);
		}
		
	    Log.w(this.getClass().getName(), "On Draw Called");
	}

}
